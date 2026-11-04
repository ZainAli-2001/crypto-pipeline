# Cost Log

Region: ap-southeast-2 · Started: 2026-10-28 · Starting credits: $140

## Weekly log

| Week ending | Files | Lambda invocations | Lambda GB-seconds | S3 storage (GB) | S3 requests | Athena data scanned | Cumulative cost (to 11-03) | Credits remaining | Surprises |
|---|---|---|---|---|---|---|---|---|---|
| 2026-10-29 (baseline) |  |  | | | | | | $140.00 | |
| 2026-11-04 | 168 | 168 scheduled (+1 rebuild) | ≈329.3 billed incl. init (≈327.3 scheduled, ≈2.0 one-off rebuild) | data 0.043, results 0.0014 | ≈336 (calculated) | B1: 16.57 KB, B2: 70.83 KB | Usage $0.00345, Credit -$0.00345, Net $0 | ≈$139.9965 (calculated) | 168 snapshots confirmed by B1. Billed ≈3.9 s/run vs ≈0.92 s Duration metric: cold-start init dominates. |
| 2026-11-11 | | | | | | | | | |
| 2026-11-18 | | | | | | | | | |
| 2026-11-25 | | | | | | | | | |

## Evidence

| Week | Checked | Cost export (CSV) | Athena B2 screenshot |
|---|---|---|---|
| 1 | 2026-11-04 | [csv](docs/cost-exports/2026-11-04-week1-cost-by-charge-type.csv) | [png](screenshots/04-athena/2026-11-04-week1-latest-snapshot-scan.png) |
| 2 | 2026-11-11 | | |

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

## Notes

**Account and credits**

- Plan: Free plan, 181 days left as of 2026-10-29.
- Starting credits are $140.

**Measurement windows**

- Cost range ends 2026-11-03 (last complete UTC day); Lambda, S3 and Athena readings were taken 2026-11-04 13:05 UTC.
- Cost (UTC days 2026-10-28 to 2026-11-03, by charge type, from CSV export): Usage $0.0034548881, Credit -$0.0034548883, Total -$0.0000000002 (rounding residue, effectively $0). Credits cover 100% of usage.
- Credits remaining is calculated (starting credits minus credit applied), not read from the credits page, which rounds.

**Budgets**

- The $5 budget excludes Credit and Refund charge types, so it tracks gross usage; the zero-spend budget has no filter, so it tracks net spend after credits.
- Consequence: the zero-spend budget will not fire while credits cover usage; the $5 budget is the real runaway-cost alarm.

**Athena**

- Athena bills a 10 MB minimum per query, so tiny scans still cost the minimum.
- B1's scan grew linearly with file count (13 files: 1.28 KB; 168 files: 16.57 KB, about 0.1 KB per file). B2 minus B1 stays near 54 KB, so the growth appears to be per-file overhead only (inferred).
- Run time shows no trend yet (B1 563 ms to 785 ms, B2 1.4 s to 931 ms). Single readings are noisy; the trend over several weeks is what matters.

**Provisional figure**

- Usage to 2026-11-03 divided by 154 snapshots is about $0.0224 per 1,000 snapshots. This includes test runs, the rebuild and my Athena queries, so it is not a pure per-snapshot cost. Recompute at the end of the run.

## Final summary (end of run)

- Total cost:
- Cost per 1,000 snapshots:
- Credits used / remaining:
- What I'd change at larger scale: