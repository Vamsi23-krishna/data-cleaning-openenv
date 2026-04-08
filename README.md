---
title: Data Cleaning OpenEnv
emoji: 🧹
colorFrom: blue
colorTo: green
sdk: docker
app_file: api/server.py
pinned: false
---

# Data Cleaning OpenEnv

A lightweight data-cleaning environment for reinforcement-style task execution using FastAPI.

## Overview

This project defines a set of data-cleaning tasks around dirty and clean CSV datasets. It exposes an API that allows clients to:

- reset a task and receive an initial observation
- submit cleaning actions
- receive rewards and updated environment state

The environment supports easy, medium, and hard tasks covering missing values, formatting normalization, and a full cleaning pipeline.

## Project Structure

- `api/server.py` - FastAPI server exposing `/reset`, `/step`, `/state`, and health endpoints.
- `env/environment.py` - Environment class that loads a dirty dataset, applies actions, computes rewards, and tracks steps.
- `env/action_handler.py` - Action implementations for cleaning operations.
- `models/action.py` - Pydantic model for typed action payloads.
- `tasks/` - Task definitions for easy, medium, and hard datasets.
- `datasets/` - Dirty and clean CSV files used by tasks.
- `inference.py` - Example script that calls the API and applies candidate actions.
- `openenv.yaml` - Environment metadata and task descriptions.

## Requirements

Install dependencies from `requirements.txt`:

```bash
pip install -r requirements.txt
```

The main dependencies are:

- `fastapi`
- `uvicorn`
- `pandas`
- `numpy`
- `py-dateutil`
- `requests`

## Running the API

Start the FastAPI server from the repository root:

```bash
uvicorn api.server:app --reload --port 8001
```

The server will run at `http://127.0.0.1:8001`.

## API Endpoints

- `POST /reset?task_id=<id>`
  - Reset the selected task environment.
  - Returns `task` and `observation`.

- `POST /step`
  - Submit an action JSON object.
  - Returns `observation`, `reward`, `done`, and `info`.

- `GET /state`
  - Query the current environment state.

- `GET /`
  - Health endpoint.

## Task List

The repository includes three tasks:

1. `easy_missing_values`
   - Fill missing values in the dataset.
2. `medium_format_cleaning`
   - Normalize dates, salary formats, and text.
3. `hard_full_pipeline`
   - Perform a full data-cleaning pipeline on a harder dataset.

Task configuration is defined in `openenv.yaml` and loaded by `tasks/task_loader.py`.

## Example Inference

After starting the server, run:

```bash
python inference.py
```

This script resets each task and attempts a series of cleaning actions while printing rewards and progress.

## How It Works

The environment tracks:

- `preview` of the current dataset state
- `missing_values`
- current `steps`

Actions include:

- `fill_missing`
- `clean_text`
- `normalize_date`
- `convert_salary`
- `remove_duplicates`

Rewards are computed by comparing the current dataset to the target clean dataset and by tracking improvements in correctness and missing values.

## Notes

- The `venv/` folder is ignored and should not be committed.
- The environment uses CSV datasets located in `datasets/`.

## License

This repository does not include a license file. Add a license if you intend to share or publish this project.
