```python
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class TaskBase(BaseModel):
    title: str = Field(..., max_length=255)
    total_duration: int = Field(..., gt=0)


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=255)
    total_duration: Optional[int] = Field(None, gt=0)


class TaskRead(TaskBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class SubtaskBase(BaseModel):
    task_id: int
    title: str = Field(..., max_length=255)
    duration: int = Field(..., gt=0)
    completed_at: Optional[datetime] = None


class SubtaskCreate(SubtaskBase):
    pass


class SubtaskUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=255)
    duration: Optional[int] = Field(None, gt=0)
    completed_at: Optional[datetime] = None


class SubtaskRead(SubtaskBase):
    id: int

    class Config:
        orm_mode = True


class TaskWithSubtasksRead(TaskRead):
    subtasks: List[SubtaskRead] = []


class SubtaskWithTaskRead(BaseModel):
    task_id: int
    task_title: str
    subtasks: List[SubtaskRead]

    class Config:
        orm_mode = True
```