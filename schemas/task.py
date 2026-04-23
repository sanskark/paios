from pydantic import BaseModel
from typing import Optional, List, Literal


class Task(BaseModel):
    task: str
    priority: Optional[str] = "medium"
    time: Optional[str] = None


class TaskList(BaseModel):
    tasks: List[Task]


class Intent(BaseModel):
    type: Literal["task", "chat"]