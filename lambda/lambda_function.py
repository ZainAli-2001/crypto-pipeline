"""
Hourly CoinGecko snapshot -> S3 (raw JSON + curated Parquet).

Env vars:
  BUCKET              (required) target S3 bucket
  SSM_PARAM_NAME      (optional) SSM parameter holding the CoinGecko key,
                      e.g. /crypto/coingecko_api_key
  COINGECKO_API_KEY   (fallback) used only if SSM_PARAM_NAME is not set

Idempotency: snapshot_ts is the scheduled time truncated to the hour, and all
S3 keys derive from it, so a retry or re-run overwrites instead of duplicating.
"""
import io
import json
import os
import re
import time
from datetime import datetime, timezone

import boto3
import pandas as pd
import requests

BASE_URL = "https://api.coingecko.com/api/v3/coins/markets"
PARAMS = {
    "vs_currency": "usd",
    "order": "market_cap_desc",
    "per_page": 250,
    "page": 1,
    "sparkline": "false",
    "price_change_percentage": "1h,24h,7d",
}
MAX_ATTEMPTS = 4
DROP_COLUMNS = ["image", "roi"]  # roi is a nested object / mostly null
TS_COLUMNS = ["ath_date", "atl_date", "last_updated"]

s3 = boto3.client("s3")
ssm = boto3.client("ssm")
_api_key_cache = None


def get_api_key():
    global _api_key_cache
    if _api_key_cache:
        return _api_key_cache
    name = os.environ.get("SSM_PARAM_NAME")
    if name:
        resp = ssm.get_parameter(Name=name, WithDecryption=True)
        _api_key_cache = resp["Parameter"]["Value"]
    else:
        _api_key_cache = os.environ["COINGECKO_API_KEY"]
    return _api_key_cache


def get_snapshot_ts(event):
    """Scheduled time from the event, truncated to the hour (UTC).

    EventBridge rules put it in event["time"]. EventBridge Scheduler sends a
    static payload, so set the target input to
    {"scheduled_time": "<aws.scheduler.scheduled-time>"}.
    Manual tests can pass either key. Falls back to now.
    """
    raw = (event or {}).get("scheduled_time") or (event or {}).get("time")
    if raw:
        ts = datetime.fromisoformat(raw.replace("Z", "+00:00"))
    else:
        ts = datetime.now(timezone.utc)
    return ts.astimezone(timezone.utc).replace(minute=0, second=0, microsecond=0)


def fetch_markets():
    headers = {"x-cg-demo-api-key": get_api_key(), "accept": "application/json"}
    for attempt in range(1, MAX_ATTEMPTS + 1):
        resp = requests.get(BASE_URL, params=PARAMS, headers=headers, timeout=15)
        if resp.status_code == 200:
            return resp.json()
        if resp.status_code == 429 and attempt < MAX_ATTEMPTS:
            wait = min(int(resp.headers.get("Retry-After", 2 ** attempt)), 10)
            print(f"429 from CoinGecko, retry {attempt} in {wait}s")
            time.sleep(wait)
            continue
        resp.raise_for_status()
    raise RuntimeError("CoinGecko fetch failed after retries")


def transform(records, snapshot_ts):
    df = pd.DataFrame(records)
    df = df.drop(columns=[c for c in DROP_COLUMNS if c in df.columns])
    for col in TS_COLUMNS:
        if col in df.columns:
            # tz-naive UTC, millisecond precision (Athena-friendly)
            df[col] = pd.to_datetime(df[col], utc=True).dt.tz_localize(None).astype("datetime64[ms]")
    # Stable schema: every numeric column is float64 (pandas would otherwise
    # pick int64 or float64 per snapshot, which breaks Athena across files).
    non_numeric = {"id", "symbol", "name", "market_cap_rank", *TS_COLUMNS}
    for col in df.columns:
        if col not in non_numeric:
            df[col] = pd.to_numeric(df[col], errors="coerce").astype("float64")
    df["market_cap_rank"] = df["market_cap_rank"].astype("Int64")
    df.insert(0, "snapshot_ts", pd.Timestamp(snapshot_ts).tz_localize(None).as_unit("ms"))
    return df


RAW_PATTERN = re.compile(r"raw/dt=(\d{4}-\d{2}-\d{2})/snapshot_(\d{4}-\d{2}-\d{2}T\d{2})\.json$")


def rebuild_from_raw(bucket):
    """One-off maintenance: rewrite every curated Parquet from its raw JSON.

    Needs temporary s3:GetObject on raw/* and s3:ListBucket (see README).
    Triggered only by the event {"rebuild_from_raw": true}.
    """
    count = 0
    for page in s3.get_paginator("list_objects_v2").paginate(Bucket=bucket, Prefix="raw/"):
        for obj in page.get("Contents", []):
            m = RAW_PATTERN.search(obj["Key"])
            if not m:
                continue
            dt, stamp = m.groups()
            snapshot_ts = datetime.strptime(stamp, "%Y-%m-%dT%H").replace(tzinfo=timezone.utc)
            records = json.loads(s3.get_object(Bucket=bucket, Key=obj["Key"])["Body"].read())
            df = transform(records, snapshot_ts)
            buf = io.BytesIO()
            df.to_parquet(buf, engine="pyarrow", index=False, compression="snappy",
                          coerce_timestamps="ms", allow_truncated_timestamps=True)
            s3.put_object(Bucket=bucket, Key=f"curated/dt={dt}/snapshot_{stamp}.parquet",
                          Body=buf.getvalue())
            print(f"rebuilt dt={dt} {stamp} ({len(df)} rows)")
            count += 1
    return {"rebuilt_files": count}


def lambda_handler(event, context):
    bucket = os.environ["BUCKET"]
    if (event or {}).get("rebuild_from_raw") is True:
        return rebuild_from_raw(bucket)
    snapshot_ts = get_snapshot_ts(event)
    dt = snapshot_ts.strftime("%Y-%m-%d")
    stamp = snapshot_ts.strftime("%Y-%m-%dT%H")

    records = fetch_markets()
    if not records:
        raise RuntimeError("CoinGecko returned no rows; refusing to write an empty snapshot")

    raw_key = f"raw/dt={dt}/snapshot_{stamp}.json"
    curated_key = f"curated/dt={dt}/snapshot_{stamp}.parquet"

    s3.put_object(
        Bucket=bucket,
        Key=raw_key,
        Body=json.dumps(records).encode("utf-8"),
        ContentType="application/json",
    )

    df = transform(records, snapshot_ts)
    buf = io.BytesIO()
    df.to_parquet(buf, engine="pyarrow", index=False, compression="snappy",
                  coerce_timestamps="ms", allow_truncated_timestamps=True)
    s3.put_object(Bucket=bucket, Key=curated_key, Body=buf.getvalue())

    result = {
        "snapshot_ts": snapshot_ts.isoformat(),
        "rows": len(df),
        "raw_key": raw_key,
        "curated_key": curated_key,
    }
    print(json.dumps(result))
    return result