from fastapi import FastAPI
from fastapi.responses import JSONResponse
from tasks.task_loader import load_all_tasks
from models.action import Action 
import math 

app = FastAPI()

tasks = load_all_tasks()
current_env = None

def clean_json(data):
    if isinstance(data, dict):
        return {k: clean_json(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [clean_json(v) for v in data]
    elif isinstance(data, float) and math.isnan(data):
        return None 
    else:
        return data 
    
@app.post("/reset")
def reset(task_id: int = 0):
    global current_env
    task = tasks[task_id]
    current_env = task["env"]
    observation = current_env.reset()
    observation = clean_json(observation)
    
    return JSONResponse(content={
        "task": task["name"],
        "observation": observation
    })

@app.post("/step")
def step(action: Action):
    global current_env 
    observation, reward, done, info = current_env.step(action)
    response = {
        "observation": observation,
        "reward": float(reward),
        "done": done,
        "info": info
    }
    response = clean_json(response)
    return JSONResponse(content=response)

@app.get("/state")
def state():
    global current_env 
    if current_env is None:
        return JSONResponse(content={"error": "Call /reset first"}, status_code=400)
    state = current_env.state()
    state = clean_json(state)
    return JSONResponse(content=state)

@app.get("/")
def home():
    return {"message": "Data Cleaning OpenEnv is running"}
