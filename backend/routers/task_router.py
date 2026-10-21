from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from sqlalchemy.orm import Session
from pydantic import BaseModel

from backend.database.session import get_db
from backend import models, schemas

router = APIRouter()

# ---------- Schemas ----------
class TaskCreate(BaseModel):
    title: str
    total_duration: int  # duration in minutes

class TaskUpdate(BaseModel):
    title: str | None = None
    total_duration: int | None = None

class TaskResponse(BaseModel):
    id: int
    title: str
    total_duration: int
    created_at: str

class SubtaskCreate(BaseModel):
    title: str
    duration: int  # duration in minutes

class SubtaskUpdate(BaseModel):
    title: str | None = None
    duration: int | None = None

class SubtaskResponse(BaseModel):
    id: int
    title: str
    duration: int
    completed_at: str | None = None

# ---------- Task Endpoints ----------
@router.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    db_task = models.Task(title=task.title, total_duration=task.total_duration)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.get("/tasks", response_model=List[TaskResponse])
def list_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Task).offset(skip).limit(limit).all()

@router.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@router.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task: TaskUpdate, db: Session = Depends(get_db)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    for key, value in task.dict(exclude_unset=True).items():
        setattr(db_task, key, value)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(db_task)
    db.commit()
    return None

# ---------- Subtask Endpoints ----------
@router.post("/tasks/{task_id}/subtasks", response_model=SubtaskResponse, status_code=status.HTTP_201_CREATED)
def create_subtask(task_id: int, subtask: SubtaskCreate, db: Session = Depends(get_db)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    db_subtask = models.Subtask(task_id=task_id, title=subtask.title, duration=subtask.duration)
    db.add(db_subtask)
    db.commit()
    db.refresh(db_subtask)
    return db_subtask

@router.get("/tasks/{task_id}/subtasks", response_model=List[SubtaskResponse])
def list_subtasks(task_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Subtask).filter(models.Subtask.task_id == task_id).offset(skip).limit(limit).all()

@router.get("/tasks/{task_id}/subtasks/{subtask_id}", response_model=SubtaskResponse)
def get_subtask(task_id: int, subtask_id: int, db: Session = Depends(get_db)):
    db_subtask = db.query(models.Subtask).filter(models.Subtask.task_id == task_id, models.Subtask.id == subtask_id).first()
    if not db_subtask:
        raise HTTPException(status_code=404, detail="Subtask not found")
    return db_subtask

@router.put("/tasks/{task_id}/subtasks/{subtask_id}", response_model=SubtaskResponse)
def update_subtask(task_id: int, subtask_id: int, subtask: SubtaskUpdate, db: Session = Depends(get_db)):
    db_subtask = db.query(models.Subtask).filter(models.Subtask.task_id == task_id, models.Subtask.id == subtask_id).first()
    if not db_subtask:
        raise HTTPException(status_code=404, detail="Subtask not found")
    for key, value in subtask.dict(exclude_unset=True).items():
        setattr(db_subtask, key, value)
    db.commit()
    db.refresh(db_subtask)
    return db_subtask

@router.delete("/tasks/{task_id}/subtasks/{subtask_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_subtask(task_id: int, subtask_id: int, db: Session = Depends(get_db)):
    db_subtask = db.query(models.Subtask).filter(models.Subtask.task_id == task_id, models.Subtask.id == subtask_id).first()
    if not db_subtask:
        raise HTTPException(status_code=404, detail="Subtask not found")
    db.delete(db_subtask)
    db.commit()
    return None