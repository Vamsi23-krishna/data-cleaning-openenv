import os
from env.environment import DataCleaningEnv

def get_easy_task():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    env = DataCleaningEnv(
        os.path.join(project_root, "datasets/easy_dirty.csv"),
        os.path.join(project_root, "datasets/easy_clean.csv")
    )
    task = {
        "name": "easy_missing_values",
        "description": "Fill missing values in dataset",
        "difficulty": "easy",
        "env": env 
    }
    return task 
