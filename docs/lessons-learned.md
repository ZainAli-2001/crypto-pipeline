# Lessons Learned

Problems and surprises from building and running the pipeline, in the order they came up. Each entry covers what happened, why, and what I did. New entries are added as the run goes on.

## 1. EventBridge Scheduler sends a static payload

**What happened.** The handler derives `snapshot_ts` (and every S3 key) from the scheduled time. EventBridge *rules* put that time in `event["time"]`, but EventBridge *Scheduler* sends whatever static payload you configure, so the handler would have fallen back to "now".

**What I did.** Set the target payload to `{"scheduled_time": "<aws.scheduler.scheduled-time>"}`. The first scheduled run produced the expected key for its hour, which confirmed the payload works.

**Takeaway.** Idempotent keys depend on the trigger carrying its own timestamp. Check what the trigger actually sends before relying on it.

## 2. Same S3 key means overwrite, not append

**What happened.** I ran the test event three times with the same fixed `scheduled_time` and expected the raw file to hold 750 entries. It held 250.

**Why.** S3 objects can't be appended to. Writing to an existing key replaces the whole object, and the deterministic key meant all three runs targeted the same one. Last modified updated each time, and only one file existed after three runs.

**Takeaway.** This is the idempotency design working as intended. The dataset grows by new hourly files, never by appending to one file.

## 3. Parquet column types can differ between files

**What happened.** pandas picks a column's type from each snapshot's data, so a column like `total_volume` is `int64` in an hour where every value is whole and `double` otherwise. Athena needs one type per column across all files, and a mix fails with `HIVE_BAD_DATA`.

**What I did.** Caught this before creating the Athena table (it never failed in a query). Cast all numeric columns to `float64` in the transform, redeployed, and rebuilt the already-written curated files. Athena then read every file without errors.

**Takeaway.** Don't let a library infer types per batch when the downstream reader needs a fixed schema. State the types explicitly.

## 4. Rebuilding curated from raw, and why raw is kept

**What happened.** A few curated files had been written before the type fix. The raw JSON for those hours was untouched, so they could be regenerated.

**What I did.** CloudShell was unavailable (blocked by an account verification issue), so I added a `rebuild_from_raw` mode to the Lambda, triggered only by the event `{"rebuild_from_raw": true}`. It needs read access the role normally lacks, so I attached a temporary read policy, ran the event (3 files rebuilt, 250 rows each), then deleted the policy.

**Takeaway.** Keeping raw next to curated makes transform bugs fixable. Temporary, narrowly scoped permissions beat widening the permanent role.

## 5. Test data labelled as a real hour

**What happened.** My manual tests used a fixed `scheduled_time` of 11:00 UTC, but the data inside was fetched later (the last test ran around 13:24 UTC). The files were labelled as an hourly snapshot that never really happened.

**What I did.** Deleted the 11:00 test files so the dataset contains only real scheduled snapshots. The first real one is 14:00 UTC on 2026-10-28.

**Takeaway.** Test output written to the production path pollutes the dataset. Delete it, or send tests somewhere separate.

## 6. A rate-based schedule counts from creation time

**What happened.** The schedule fires at about two minutes past each hour, not exactly on it, because a rate-based schedule counts from the moment it was created and the start time field was left blank.

**Why it's harmless.** The handler truncates the scheduled time to the hour, so a run at 19:02 writes the 19:00 key.

## 7. Budgets can read differently from the same spend

**What happened.** My two budgets showed different percentages for the same account. The $5 budget excludes the *Credit* and *Refund* charge types, so it counts gross usage; the zero-spend budget has no filter, so it counts net spend after credits.

**What I did.** Confirmed in Cost Explorer (grouped by charge type): Usage $0.00125364, Credit -$0.00125364, Total $0. The gross figure matches the $5 budget's 99.98% remaining.

**Takeaway.** The zero-spend budget stays quiet while credits cover usage, so the $5 budget is the real runaway-cost alarm. Cost Explorer's default view rounds to cents and showed $0.00 everywhere. The table view shows the real digits.

## 8. Athena shows `-` for data scanned on DDL

**What happened.** `CREATE VIEW` showed no data scanned, which looked like missing cost information.

**Why.** DDL reads no data. Scan figures appear only when the view is queried. A `SELECT * FROM latest_snapshot` over 13 files scanned 56.06 KB, and Athena bills a 10 MB minimum per query, so queries at this scale all cost the minimum.

## 9. Budget alert emails show "Pending" verification

**What I observed.** The notification email on the budgets shows as pending verification, so alert emails may not be delivered. Status as of 2026-10-29: unresolved.

**What I did.** Treat the weekly manual check (Cost Explorer by charge type, see `cost-log.md`) as the real safeguard, not the alerts.

**Takeaway.** An alert that may not arrive isn't a control. Keep a manual check on a fixed day each week.