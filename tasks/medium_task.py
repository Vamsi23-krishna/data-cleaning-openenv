import os
from env.environment import DataCleaningEnv

def get_medium_task():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    env = DataCleaningEnv(
        os.path.join(project_root, "datasets/medium_dirty.csv"),
        os.path.join(project_root, "datasets/medium_clean.csv")
    )
    task = {
        "name": "medium_format_cleaning",
        "description": "Normalize dates, text, and salary formats",
        "difficulty": "medium",
        "env": env 
    }
    return task 