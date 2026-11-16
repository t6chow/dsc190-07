# DSC 190 Assignment 07: Reproducible Data Pipelines

A DVC pipeline that cleans and featurizes `data/raw/events.csv`, plus a Marimo
notebook that plots the distribution of event durations.

## Usage

```bash
uv sync
uv run dvc repro                          # clean -> transform -> features
uv run marimo edit notebooks/report.py    # view the report
```

## Pipeline

| Stage       | Input                         | Output                        |
|-------------|-------------------------------|-------------------------------|
| `clean`     | `data/raw/events.csv`         | `data/clean/events.csv`       |
| `transform` | `data/clean/events.csv`       | `data/transformed/events.csv` |
| `features`  | `data/transformed/events.csv` | `data/features/events.csv`    |
