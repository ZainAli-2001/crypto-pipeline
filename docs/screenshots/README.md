# Screenshots

Proof and reference images for the pipeline. Captions live where the images
are used (`README.md`, `docs/cost-log.md`); the filenames describe each shot.

## Layout

One folder per topic, numbered in build order:

| Folder | Contents |
|---|---|
| `01-eventbridge/` | Schedule configuration and target payload |
| `02-lambda/` | Function configuration and role policies |
| `03-s3/` | Raw and curated files in the data bucket |
| `04-athena/` | Query results and data scanned |
| `05-budget/` | Budget list, filters and scope |
| `06-billing/` | Cost Explorer by charge type, credits, weekly readings |

## Naming

`YYYY-MM-DD-what-it-shows.png`, lowercase with hyphens. Weekly cost shots
include the week: `2026-11-04-week1-cost-by-charge-type.png`.

## Redaction

Account ID, email and bucket names are covered before committing.
Unedited originals are kept outside the repo.

## Notes on what you'll see

**Closely spaced Last modified times on early curated files.**
Some files were written minutes apart, or re-written later. These come from
my test invocations (run with a fixed `scheduled_time`, which overwrote the
same key) and from a one-off rebuild of curated files from raw after I fixed
a Parquet type-consistency issue. The scheduled hourly runs began on
2026-10-28 (first real snapshot: 14:00 UTC). Test files for the 11:00 slot
were deleted.