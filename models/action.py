from pydantic import BaseModel
from typing import Optional 

class Action(BaseModel):
    action_type: str
    column: Optional[str] = None
    value: Optional[str] = None 