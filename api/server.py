from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn
import os
import math

from tasks.task_loader import load_all_tasks
from models.action import Action

app = FastAPI(title="Data Cleaning OpenEnv")

tasks = load_all_tasks()
current_env = None


def clean_json(data):
    """Helper to convert NaN values to None for JSON compatibility"""
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
    if current_env is None:
        return JSONResponse(
            content={"error": "Call /reset first"}, 
            status_code=400
        )
    
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
        return JSONResponse(
            content={"error": "Call /reset first"}, 
            status_code=400
        )
    state_data = current_env.state()
    state_data = clean_json(state_data)
    return JSONResponse(content=state_data)


@app.get("/")
def home():
    return {"message": "Data Cleaning OpenEnv is running"}


# Hugging Face Spaces prefixed routes
@app.post("/spaces/{owner}/{repo}/reset")
def reset_prefixed(owner: str, repo: str, task_id: int = 0):
    return reset(task_id)


@app.post("/spaces/{owner}/{repo}/step")
def step_prefixed(owner: str, repo: str, action: Action):
    return step(action)


@app.get("/spaces/{owner}/{repo}/state")
def state_prefixed(owner: str, repo: str):
    return state()


@app.get("/spaces/{owner}/{repo}/")
def home_prefixed(owner: str, repo: str):
    return home()


# ====================== MAIN ENTRY POINT (Fixed for HF Spaces) ======================
def main():
    """Entry point for uv run server, Docker, and Hugging Face Spaces"""
    # Hugging Face Spaces uses $PORT environment variable, default to 7860
    port = int(os.getenv("PORT", 7860))
    
    uvicorn.run(
        "api.server:app",      # Must be string when used as entry point
        host="0.0.0.0",        # Required for Docker / external access
        port=port,
        reload=False
    )


if __name__ == "__main__":
    main()