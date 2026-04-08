import os
from env.environment import DataCleaningEnv

def get_hard_task():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    env = DataCleaningEnv(
        os.path.join(project_root, "datasets/hard_dirty.csv"),
        os.path.join(project_root, "datasets/hard_clean.csv")
    )
    task = {
        "name": "hard_full_pipeline",
        "description": "Perform full data cleaning pipeline",
        "difficulty": "hard",
        "env": env 
    }
    return task