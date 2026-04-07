import pandas as pd 
from env.action_handler import apply_action
from models.action import Action

class DataCleaningEnv:
    def __init__(self, dataset_path, clean_path):
        self.dataset_path = dataset_path
        self.clean_path = clean_path
        self.df = None
        self.clean_df = None
        self.steps = 0
        self.max_steps = 10

    def reset(self):
        self.df = pd.read_csv(self.dataset_path)
        self.clean_df = pd.read_csv(self.clean_path)
        self.steps = 0
        return self._get_observation()
    
    def step(self, action: Action):
        self.steps += 1
        prev_df = self.df.copy()
        try:
            self.df = apply_action(self.df, action)
        except Exception as e:
            print("ERROR:", e)
            return self._get_observation(), -0.2, False, {"error": str(e)}
        reward = self._calculate_reward(prev_df, action)
        done = self._check_done()
        return self._get_observation(), reward, done, {"steps": self.steps}
    
    def state(self):
        df_clean = self.df.copy()
        df_clean = df_clean.astype(object).where(df_clean.notnull(), None)
        return {
            "data": df_clean.to_dict(),
            "steps": self.steps 
        }
    
    def _get_observation(self):
        df_clean = self.df.copy()
        df_clean = df_clean.astype(object).where(df_clean.notnull(), None)
        return {
            "preview": df_clean.to_dict(),
            "missing_values": self.df.isnull().sum().to_dict(),
            "steps": self.steps 
        }
    
    def _calculate_reward(self, prev_df, action):
        try:
           total = self.df.size 
           df_current = self.df.fillna("NA")
           df_clean = self.clean_df.fillna("NA")
           df_prev = prev_df.fillna("NA")
           prev_correct = (df_prev == df_clean).sum().sum()
           new_correct = (df_current == df_clean).sum().sum()
           improvement = new_correct - prev_correct
           prev_missing = prev_df.isnull().sum().sum()
           new_missing = self.df.isnull().sum().sum()
           missing_improvement = prev_missing - new_missing
           reward = 0.0
           reward += improvement / total 
           reward += 0.2 * missing_improvement
           
           # Special handling for format conversion actions
           if action.action_type == "convert_salary":
               if improvement > 0:
                   pass  # Keep improvement reward
               else:
                   reward = 0.15  # Match Task 1's convert_salary reward
           elif action.action_type == "normalize_date":
               if improvement > 0:
                   pass  # Keep improvement reward
               else:
                   reward = 0.1  # Match Task 1's normalize_date reward
           elif improvement == 0 and missing_improvement == 0:
               reward -= 0.1
               
           if self.df.equals(self.clean_df):
               reward += 1.0
           return float(reward)
        except Exception:
            # For structural cleanup actions like remove_duplicates, return positive bonus
            if action.action_type == "remove_duplicates":
                return 0.1
            return -0.1
    def _check_done(self):
        if self.steps >= self.max_steps:
            return True 
        if self.df.equals(self.clean_df):
            return True 
        return False
    
