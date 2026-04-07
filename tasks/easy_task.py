from env.environment import DataCleaningEnv

def get_easy_task():
    env = DataCleaningEnv(
        "datasets/easy_dirty.csv",
        "datasets/easy_clean.csv"
    )
    task = {
        "name": "easy_missing_values",
        "description": "Fill missing values in dataset",
        "difficulty": "easy",
        "env": env 
    }
    return task 
