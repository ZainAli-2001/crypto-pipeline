# Cost Log

Region: ap-southeast-2 · Started: 2026-10-28 · Starting credits: $140

## Weekly log

| Week ending | Files | Lambda invocations | Lambda GB-seconds | S3 storage (GB) | S3 requests | Athena data scanned | Cumulative cost (to 11-10) | Credits remaining | Surprises |
|---|---|---|---|---|---|---|---|---|---|
| 2026-10-29 (baseline) | - | - | - | - | - | - | - | $140.00 | |
| 2026-11-04 | 168 | 168 scheduled (+1 rebuild) | ≈329.3 billed incl. init (≈327.3 scheduled, ≈2.0 one-off rebuild) | data 0.043, results 0.00011 | ≈336 (calculated) | B1: 16.57 KB, B2: 70.83 KB | Usage $0.00345, Credit -$0.00345, Net $0 | ≈$139.9965 (calculated) | 168 snapshots confirmed by B1. Billed ≈3.9 s/run vs ≈0.92 s Duration metric: cold-start init dominates. |
| 2026-11-11 | 168 | 168 scheduled | ≈321.4 billed incl. init (≈3.8 s/run) | data 0.078, results 0.00022 | ≈336 (calculated) | B1: 33.14 KB, B2: 87.47 KB | Usage $0.00592, Credit -$0.00592, Net $0 | ≈$139.9941 (calculated) | B1 scan doubled with file count (16.57 to 33.14 KB). B2 minus B1 steady at about 54 KB. Week 1 cost export was partial, see Notes. |
| 2026-11-18 | | | | | | | | | |
| 2026-11-25 | | | | | | | | | |

## Evidence

| Week | Checked | Cost export (CSV) | Athena B2 screenshot |
|---|---|---|---|
| 1 | 2026-11-04 | [csv](cost-exports/2026-11-04-week1-cost-by-charge-type.csv) | [png](screenshots/04-athena/2026-11-04-week1-latest-snapshot-scan.png) |
| 2 | 2026-11-11 | [csv](cost-exports/2026-11-11-week2-cost-by-charge-type.csv)  | [png](screenshots/04-athena/2026-11-11-week2-latest-snapshot-scan.png) |
| 3 | 2026-11-18 | | |

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

## Notes

**Account and credits**

- Plan: Free plan, 181 days left as of 2026-10-29.
- Starting credits are $140.

**Measurement windows**

- Standing rules: cost figures are cumulative from 2026-10-28 and end at the
  last complete UTC day. Lambda, S3 and Athena readings are taken at about
  13:05 UTC on the check date. Credits remaining is calculated (starting
  credits minus credit applied), not read from the credits page, which rounds.

| Week | Cost range (UTC days) | Readings taken (UTC) |
|---|---|---|
| 1 | 2026-10-28 to 2026-11-03 | 2026-11-04 13:05 |
| 2 | 2026-10-28 to 2026-11-10 | 2026-11-11 13:05 |

- Cost (UTC days 2026-10-28 to 2026-11-03, by charge type, from CSV export): Usage $0.0034548881, Credit -$0.0034548883, Total -$0.0000000002 (rounding residue, effectively $0). Credits cover 100% of usage.
- Cost (UTC days 2026-10-28 to 2026-11-10, by charge type, from CSV export): Usage $0.005921261, Credit -$0.005921261, Total -$0.0000000006 (rounding residue, effectively $0). Credits cover 100% of usage. 


**Budgets**

- The $5 budget excludes Credit and Refund charge types, so it tracks gross usage; the zero-spend budget has no filter, so it tracks net spend after credits.
- Consequence: the zero-spend budget will not fire while credits cover usage; the $5 budget is the real runaway-cost alarm.
- Week 1 cost export was taken before 1 Nov usage had fully posted. The 1 Nov
  line now reads $0.00337, so the week 1 total of $0.00345 was understated.
  The week 2 cumulative export supersedes it: usage $0.0059212606 to 2026-11-10.

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