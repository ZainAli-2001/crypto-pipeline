# Cost Log

Region: ap-southeast-2 · Started: 2026-10-28 · Starting credits: $140

## Weekly log

| Week ending | Files | Lambda invocations | Lambda GB-seconds | S3 storage (GB) | S3 requests | Athena data scanned | Cumulative cost (to 11-24) | Credits remaining | Surprises |
|---|---|---|---|---|---|---|---|---|---|
| 2026-10-29 (baseline) | - | - | - | - | - | - | - | $140.00 | |
| 2026-11-04 | 168 | 168 scheduled (+1 rebuild) | ≈329.3 billed incl. init (≈327.3 scheduled, ≈2.0 one-off rebuild) | data 0.043 (metric, 4 Nov; low, see Notes), results 0.00011 | ≈336 (calculated) | B1: 16.57 KB, B2: 70.83 KB | Usage $0.00345, Credit -$0.00345, Net $0 | ≈$139.9965 (calculated) | 168 snapshots confirmed by B1. Billed ≈3.9 s/run vs ≈0.92 s Duration metric: cold-start init dominates. |
| 2026-11-11 | 168 | 168 scheduled | ≈321.4 billed incl. init (≈3.8 s/run) | 0.104 (11 Nov, metric), results 0.00022 | ≈336 (calculated) | B1: 33.14 KB, B2: 87.47 KB | Usage $0.00592, Credit -$0.00592, Net $0 | ≈$139.9941 (calculated) | B1 scan doubled with file count (16.57 to 33.14 KB). B2 minus B1 steady at about 54 KB. Week 1 cost export was partial, see Notes. |
| 2026-11-18 | 504 total (168 this week) | 168 scheduled | ≈315.4 billed incl. init (≈3.76 s/run) | 0.152 (18 Nov, object total, matches metric), results 0.00033 | ≈336 (calculated) | B1: 49.71 KB, B2: 104.01 KB | Usage $0.00978, Credit -$0.00978, Net $0 | ≈$139.9902 (calculated) | Billed time per run stable (3.8 to 3.76 s). B1 scan 33.14 to 49.71 KB as files went 336 to 504. B2 minus B1 steady at about 54 KB. |
| 2026-11-25 | 672 total (168 this week) | 168 scheduled | ≈317.5 billed incl. init (≈3.78 s/run) | data 0.206 (object total), results 0.00056 | ≈336 (calculated) | B1: 66.28 KB, B2: 120.51 KB | Usage $0.01373, Credit -$0.01373, Net $0 | ≈$139.9863 (calculated) | Billed time per run flat for four weeks (3.8 to 3.78 s). Data metric lagged about 2.5 days' growth this week. B1 scan up with file count (49.71 to 66.28 KB). |
| 2026-11-27 | | | | | | | | | |

## Evidence

| Week | Checked | Cost export (CSV) | Athena B2 screenshot |
|---|---|---|---|
| 1 | 2026-11-04 | [csv](cost-exports/2026-11-04-week1-cost-by-charge-type.csv) | [png](screenshots/04-athena/2026-11-04-week1-latest-snapshot-scan.png) |
| 2 | 2026-11-11 | [csv](cost-exports/2026-11-11-week2-cost-by-charge-type.csv)  | [png](screenshots/04-athena/2026-11-11-week2-latest-snapshot-scan.png) |
| 3 | 2026-11-18 | [csv](cost-exports/2026-11-18-week3-cost-by-charge-type.csv) | [png](screenshots/04-athena/2026-11-18-week3-latest-snapshot-scan.png) |
| 4 | 2026-11-25 | [csv](cost-exports/2026-11-25-week4-cost-by-charge-type.csv) | [png](screenshots/04-athena/2026-11-25-week4-latest-snapshot-scan.png) |
| 4 | 2026-11-27 | | |

## Benchmark queries

| ID | Query |
|---|---|
| B1 | `SELECT snapshot_ts, count(*) AS coins FROM crypto_pipeline.crypto_hourly_records GROUP BY snapshot_ts ORDER BY snapshot_ts` |
| B2 | `SELECT * FROM crypto_pipeline.latest_snapshot` |

## Spot readings

| Date | Query | Data scanned | Run time |
|---|---|---|---|
| 2026-10-29 | B1 | 1.28 KB | 563 ms |
| 2026-10-29 | B2 | 56 KB | 1.4 s |
| 2026-11-04 | B1 | 16.57 KB | 785 ms |
| 2026-11-04 | B2 | 70.83 KB | 931 ms |
| 2026-11-11 | B1 | 33.14 KB | 715 ms |
| 2026-11-11 | B2 | 87.47 KB | 1.489 s |
| 2026-11-18 | B1 | 49.71 KB | 622 ms |
| 2026-11-18 | B2 | 104.01 KB | 1.376 s |
| 2026-11-25 | B1 | 66.28 KB | 1.412 s |
| 2026-11-25 | B2 | 120.51 KB | 1.436 s |

## Notes

**Account and credits**

- Plan: Free plan, 181 days left as of 2026-10-29.
- Starting credits are $140.

**Measurement windows**

- Standing rules: cost figures are cumulative from 2026-10-28 and end at the
  last complete UTC day. Lambda, S3 and Athena readings are taken at about
  13:05 UTC on the check date. S3 storage (GB) is accumulated number while 
  rest are weekly. Credits remaining is calculated (starting credits minus 
  credit applied), not read from the credits page, which rounds.
- S3 storage: the object total (Calculate total size on `raw/` and `curated/`,
  selected together) is the reference. The BucketSizeBytes metric (Maximum,
  1-day, StandardStorage) is a cross-check only. Its lag varies: it matched
  on 18 Nov, but was about 19.5 MB low on 25 Nov.

| Week | Cost range (UTC days) | Readings taken (UTC) |
|---|---|---|
| 1 | 2026-10-28 to 2026-11-03 | 2026-11-04 13:05 |
| 2 | 2026-10-28 to 2026-11-10 | 2026-11-11 13:05 |
| 3 | 2026-10-28 to 2026-11-17 | 2026-11-18 13:05 |
| 4 | 2026-10-28 to 2026-11-24 | 2026-11-25 13:05 |

- Cost (UTC days 2026-10-28 to 2026-11-03, by charge type, from CSV export): Usage $0.0034548881, Credit -$0.0034548883, Total -$0.0000000002 (rounding residue, effectively $0). Credits cover 100% of usage.
- Cost (UTC days 2026-10-28 to 2026-11-10, by charge type, from CSV export): Usage $0.005921261, Credit -$0.005921261, Total -$0.0000000006 (rounding residue, effectively $0). Credits cover 100% of usage. 
- Cost (UTC days 2026-10-28 to 2026-11-17, by charge type, from CSV export): Usage $0.009784019, Credit -$0.009784020, Total -$0.0000000013 (rounding residue, effectively $0). Credits cover 100% of usage.
- Cost (UTC days 2026-10-28 to 2026-11-24, by charge type, from CSV export): Usage $0.013731069, Credit -$0.013731070, Total -$0.0000000016 (rounding residue, effectively $0). Credits cover 100% of usage.

**Budgets**

- The $5 budget excludes Credit and Refund charge types, so it tracks gross usage; the zero-spend budget has no filter, so it tracks net spend after credits.
- Consequence: the zero-spend budget will not fire while credits cover usage; the $5 budget is the real runaway-cost alarm.

**Athena**

- Athena bills a 10 MB minimum per query, so tiny scans still cost the minimum.
- B1's scan grew linearly with file count (13 files: 1.28 KB; 168 files: 16.57 KB, about 0.1 KB per file). B2 minus B1 stays near 54 KB, so the growth appears to be per-file overhead only (inferred).
- Run time shows no trend yet (B1 563 ms to 785 ms, B2 1.4 s to 931 ms). Single readings are noisy; the trend over several weeks is what matters.

**Provisional figure**

- Usage to 2026-11-10 ($0.0059212606) divided by 322 snapshots (28 Oct 14:00 to 10 Nov 23:00 UTC) is about $0.0184 per 1,000 snapshots. This supersedes the week 1 figure of $0.0224, which used an export taken before 1 Nov usage had posted. It includes test runs, the rebuild and my Athena queries, so it is not a pure per-snapshot cost. Recompute at the end of the run.

## Final summary (end of run)

- Total cost:
- Cost per 1,000 snapshots:
- Credits used / remaining:
- What I'd change at larger scale: