# Cost Log

Region: ap-southeast-2 · Started: 2026-10-28 · Starting credits: $140

## Weekly log

| Week ending | Files | Lambda invocations | Lambda GB-seconds | S3 storage (GB) | S3 requests | Athena data scanned | Credits remaining | Surprises |
|---|---|---|---|---|---|---|---|---|
| 2026-10-29 (baseline) | | | | | | | $140.00 | Free plan, 181 days left |
| 2026-11-04 | | | | | | | | |
| 2026-11-11 | | | | | | | | |
| 2026-11-18 | | | | | | | | |
| 2026-11-25 | | | | | | | | |

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

## Notes

- Athena bills a 10 MB minimum per query, so tiny scans still cost the minimum.
- Budgets: the $5 budget excludes Credit and Refund charge types, so it
  tracks gross usage; the zero-spend budget has no filter, so it tracks net
  spend after credits. Confirmed in Cost Explorer (Oct 1-29, by charge
  type): Usage $0.00125364, Credit -$0.00125364, Total $0. That gross
  figure matches the $5 budget's 99.98% remaining.
- Consequence: the zero-spend budget will not fire while credits cover
  usage; the $5 budget is the real runaway-cost alarm.

## Final summary (end of run)

- Total cost:
- Cost per 1,000 snapshots:
- Credits used / remaining:
- What I'd change at larger scale: