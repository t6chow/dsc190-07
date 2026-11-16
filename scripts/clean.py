"""Clean the raw events data.

Drops rows with missing fields, invalid event types, or non-positive
durations, and normalizes timestamps to ISO 8601 (YYYY-MM-DDTHH:MM:SS).
"""

from pathlib import Path

import pandas as pd

INPUT = Path("data/raw/events.csv")
OUTPUT = Path("data/clean/events.csv")

VALID_EVENT_TYPES = {"click", "login", "purchase", "scroll", "view"}

TIMESTAMP_FORMATS = [
    "%Y-%m-%dT%H:%M:%S",
    "%Y-%m-%dT%H:%M:%S.%f",
    "%Y-%m-%d %H:%M:%S",
    "%m/%d/%Y %H:%M:%S",
]


def parse_timestamp(value: str) -> pd.Timestamp:
    for fmt in TIMESTAMP_FORMATS:
        try:
            return pd.to_datetime(value, format=fmt)
        except ValueError:
            continue
    return pd.NaT


def main() -> None:
    df = pd.read_csv(INPUT, dtype=str)

    df = df.dropna()
    df = df[df["event_type"].isin(VALID_EVENT_TYPES)]

    df["duration_seconds"] = pd.to_numeric(df["duration_seconds"], errors="coerce")
    df = df[df["duration_seconds"] > 0]
    df["duration_seconds"] = df["duration_seconds"].astype(int)

    timestamps = df["timestamp"].map(parse_timestamp)
    df = df[timestamps.notna()]
    df["timestamp"] = timestamps[timestamps.notna()].dt.strftime("%Y-%m-%dT%H:%M:%S")

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT, index=False)


if __name__ == "__main__":
    main()
