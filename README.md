---
title: Data Cleaning OpenEnv
emoji: 🧹
colorFrom: blue
colorTo: green
sdk: docker
sdk_version: "1.0"
python_version: "3.10"
app_file: api/server.py
pinned: false
---

# Data Cleaning OpenEnv

A lightweight data-cleaning environment for reinforcement-style task execution using FastAPI.

[![Hugging Face Spaces](https://img.shields.io/badge/🤗%20Hugging%20Face-Spaces-blue)](https://huggingface.co/spaces/Vamsi23-krishna/data-cleaning-openenv)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-black)](https://github.com/Vamsi23-krishna/data-cleaning-openenv)

## Problem

Data cleaning is a critical but often tedious and error-prone step in machine learning pipelines. Traditional approaches require manual intervention and domain expertise, making them:

- **Time-consuming**: Manual data cleaning can take up to 80% of a data scientist's time
- **Error-prone**: Human mistakes in data preprocessing lead to poor model performance
- **Inconsistent**: Different team members may apply different cleaning strategies
- **Not scalable**: Manual processes don't scale to large datasets or frequent updates

This project addresses these challenges by providing a **reinforcement learning environment** for automated data cleaning, where agents can learn optimal cleaning strategies through trial and error.

### Key Challenges Addressed

1. **Missing Value Handling**: Automatically detect and fill missing values appropriately
2. **Data Type Normalization**: Convert inconsistent formats (dates, currencies, text)
3. **Duplicate Detection**: Identify and remove duplicate records
4. **Text Standardization**: Normalize text casing and spacing
5. **Pipeline Optimization**: Learn the optimal sequence of cleaning operations

## Architecture

### Core Components

```
Data Cleaning OpenEnv
├── API Layer (FastAPI)
│   ├── /reset - Initialize environment
│   ├── /step - Execute cleaning action
│   └── /state - Get current state
├── Environment Engine
│   ├── DataCleaningEnv - Core RL environment
│   ├── Action Handler - Cleaning operations
│   └── Reward System - Performance evaluation
├── Task Management
│   ├── Easy Task - Missing value handling
│   ├── Medium Task - Format normalization
│   └── Hard Task - Full cleaning pipeline
└── Datasets
    ├── Dirty CSV files (input)
    └── Clean CSV files (ground truth)
```

### Environment Design

The environment follows the standard OpenAI Gym interface:

- **Observation Space**: Dictionary containing:
  - `preview`: Current dataset state (with NaN handling)
  - `missing_values`: Count of missing values per column
  - `steps`: Current step count

- **Action Space**: Dictionary with:
  - `action_type`: One of 5 cleaning operations
  - `column`: Target column (when applicable)

- **Reward System**:
  - **Improvement Reward**: Based on data quality improvement (0-1 scale)
  - **Completion Bonus**: +1.0 for achieving perfect dataset
  - **Penalty**: -0.1 for ineffective actions
  - **Special Bonuses**: Format conversion rewards (0.1-0.2)

### Action Types

1. **`fill_missing`** - Fill missing values with mean (numeric) or "unknown" (categorical)
2. **`clean_text`** - Strip whitespace and convert to lowercase
3. **`normalize_date`** - Convert dates to YYYY-MM-DD format
4. **`convert_salary`** - Remove currency symbols and convert to numeric
5. **`remove_duplicates`** - Remove duplicate rows (excluding ID column)

## Usage

### Quick Start

#### 1. Local Development

```bash
# Clone the repository
git clone https://github.com/Vamsi23-krishna/data-cleaning-openenv.git
cd data-cleaning-openenv

# Install dependencies
pip install -r requirements.txt

# Start the API server
python -m uvicorn api.server:app --host 127.0.0.1 --port 8000

# In another terminal, run inference
python inference.py
```

#### 2. Docker Deployment

```bash
# Build and run with Docker
docker build -t data-cleaning-env .
docker run -p 8000:7860 data-cleaning-env
```

#### 3. Hugging Face Spaces

The environment is deployed on Hugging Face Spaces:
- **Live Demo**: https://huggingface.co/spaces/Vamsi23-krishna/data-cleaning-openenv
- **API Endpoints**: Available at the Space URL

### API Reference

#### POST `/reset?task_id=<0|1|2>`
Initialize a specific task environment.

**Response:**
```json
{
  "task": "easy_missing_values",
  "observation": {
    "preview": {...},
    "missing_values": {"column": count},
    "steps": 0
  }
}
```

#### POST `/step`
Execute a cleaning action.

**Request Body:**
```json
{
  "action_type": "fill_missing|clean_text|normalize_date|convert_salary|remove_duplicates",
  "column": "column_name"  // Optional for remove_duplicates
}
```

**Response:**
```json
{
  "observation": {...},
  "reward": 0.4,
  "done": false,
  "info": {"steps": 1}
}
```

#### GET `/state`
Get current environment state.

**Response:**
```json
{
  "data": {...},
  "steps": 5
}
```

#### GET `/`
Health check endpoint.

**Response:**
```json
{"message": "Data Cleaning OpenEnv is running"}
```

### Validation

Run comprehensive validation:

```bash
# Validate project structure and functionality
python openenv.py validate

# Test all endpoints
python test_endpoints.py
```

## Results

### Performance Metrics

The environment has been validated across all three difficulty levels:

| Task | Difficulty | Actions | Score | Status |
|------|------------|---------|-------|--------|
| **Task 0** | Easy | 5 actions | **1.05** | ✅ Complete |
| **Task 1** | Medium | 5 actions | **1.10** | ✅ Complete |
| **Task 2** | Hard | 6 actions | **1.30** | ✅ Complete |

### Action Effectiveness

**Reward Distribution by Action Type:**

- `fill_missing`: 0.2-0.5 (effective missing value handling)
- `convert_salary`: 0.15-0.16 (successful format conversion)
- `normalize_date`: 0.1-0.12 (date standardization)
- `clean_text`: 0.15-0.32 (text normalization)
- `remove_duplicates`: 0.1 (duplicate removal)

### Dataset Characteristics

**Easy Task**: 4 rows × 5 columns (id, name, age, date, salary)
- Focus: Missing value imputation and basic format conversion
- Issues: Missing age and salary values, inconsistent salary formats
- Primary actions: `fill_missing`, `convert_salary`

**Medium Task**: 4 rows × 5 columns (id, name, age, date, salary)
- Focus: Format normalization across multiple data types
- Issues: Inconsistent date formats, mixed text casing, currency symbols
- Primary actions: `normalize_date`, `convert_salary`, `clean_text`

**Hard Task**: 6 rows × 5 columns → 5 rows × 5 columns (after deduplication)
- Focus: Complete pipeline including duplicate removal
- Issues: All format inconsistencies + duplicate records, missing values
- Primary actions: All actions including `remove_duplicates`

### Validation Results

**Structure Validation**: ✅ 18/18 files present
**Import Validation**: ✅ 7/7 modules importable
**Functional Testing**: ✅ All endpoints operational
**Inference Testing**: ✅ All tasks solvable

### Deployment Status

- **Local**: ✅ Fully functional
- **Docker**: ✅ Containerized deployment
- **Hugging Face Spaces**: ✅ Live deployment
- **GitHub**: ✅ Source code repository

### Key Achievements

1. **Complete RL Environment**: Full OpenAI Gym-compatible interface
2. **Comprehensive Action Set**: 5 distinct data cleaning operations
3. **Progressive Difficulty**: Easy → Medium → Hard task progression
4. **Robust Reward System**: Meaningful feedback for learning agents
5. **Production Ready**: Deployed and accessible via API
6. **Well Documented**: Complete validation and usage examples

## Project Structure

```
data_cleaning_openenv/
├── api/
│   ├── __init__.py
│   └── server.py              # FastAPI server
├── env/
│   ├── __init__.py
│   ├── environment.py         # Core RL environment
│   └── action_handler.py      # Cleaning operations
├── models/
│   ├── __init__.py
│   └── action.py              # Pydantic models
├── tasks/
│   ├── __init__.py
│   ├── easy_task.py           # Task 0 definition
│   ├── medium_task.py         # Task 1 definition
│   └── hard_task.py           # Task 2 definition
├── utils/
│   ├── __init__.py
│   ├── actions_list.py        # Available actions
│   └── validators.py          # Action validation
├── graders/
│   ├── __init__.py
│   └── grader.py              # Scoring utilities
├── datasets/
│   ├── easy_dirty.csv         # Task 0 input
│   ├── easy_clean.csv         # Task 0 target
│   ├── medium_dirty.csv       # Task 1 input
│   ├── medium_clean.csv       # Task 1 target
│   ├── hard_dirty.csv         # Task 2 input
│   └── hard_clean.csv         # Task 2 target
├── inference.py               # Example inference script
├── openenv.py                 # CLI validation tool
├── test_endpoints.py          # API testing script
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Container configuration
├── openenv.yaml               # Environment metadata
├── README.md                  # This file
├── DEPLOYMENT.md              # Deployment checklist
└── VALIDATION_REPORT.md       # Validation results
```

## Requirements

Install dependencies:

```bash
pip install -r requirements.txt
```

**Core Dependencies:**
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `pandas` - Data manipulation
- `numpy` - Numerical operations
- `python-dateutil` - Date parsing

**Development Dependencies:**
- `requests` - HTTP client (for testing and inference scripts)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run validation: `python openenv.py validate`
5. Test inference: `python inference.py`
6. Submit a pull request

## License

This project is open source and available under the MIT License.

## Citation

If you use this environment in your research, please cite:

```bibtex
@misc{data-cleaning-openenv,
  title={Data Cleaning OpenEnv: A Reinforcement Learning Environment for Automated Data Cleaning},
  author={Krishna, Vamsi},
  year={2026},
  url={https://github.com/Vamsi23-krishna/data-cleaning-openenv}
}
```
