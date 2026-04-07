from env.environment import DataCleaningEnv

def get_hard_task():
    env = DataCleaningEnv(
        "datasets/hard_dirty.csv",
        "datasets/hard_clean.csv"
    )
    task = {
        "name": "hard_full_pipeline",
        "description": "Perform full data cleaning pipeline",
        "difficulty": "hard",
        "env": env 
    }
    return task