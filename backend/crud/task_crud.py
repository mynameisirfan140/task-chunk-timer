```python
from typing import List, Optional

from sqlalchemy.orm import Session

from ..models.task_model import Task, Subtask
from ..schemas.task_schema import TaskCreate, TaskUpdate, SubtaskCreate, SubtaskUpdate


def create_task(db: Session, obj_in: TaskCreate) -> Task:
    db_task = Task(**obj_in.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def get_task(db: Session, task_id: int) -> Optional[Task]:
    return db.query(Task).filter(Task.id == task_id).first()


def get_tasks(db: Session, skip: int = 0, limit: int = 100) -> List[Task]:
    return db.query(Task).offset(skip).limit(limit).all()


def update_task(db: Session, task_id: int, obj_in: TaskUpdate) -> Optional[Task]:
    db_task = get_task(db, task_id)
    if not db_task:
        return None
    data = obj_in.dict(exclude_unset=True)
    for field, value in data.items():
        setattr(db_task, field, value)
    db.commit()
    db.refresh(db_task)
    return db_task


def delete_task(db: Session, task_id: int) -> bool:
    db_task = get_task(db, task_id)
    if not db_task:
        return False
    db.delete(db_task)
    db.commit()
    return True


def create_subtask(db: Session, obj_in: SubtaskCreate, task_id: int) -> Subtask:
    db_subtask = Subtask(task_id=task_id, **obj_in.dict())
    db.add(db_subtask)
    db.commit()
    db.refresh(db_subtask)
    return db_subtask


def get_subtask(db: Session, subtask_id: int) -> Optional[Subtask]:
    return db.query(Subtask).filter(Subtask.id == subtask_id).first()


def get_subtasks_by_task(db: Session, task_id: int) -> List[Subtask]:
    return db.query(Subtask).filter(Subtask.task_id == task_id).all()


def update_subtask(db: Session, subtask_id: int, obj_in: SubtaskUpdate) -> Optional[Subtask]:
    db_subtask = get_subtask(db, subtask_id)
    if not db_subtask:
        return None
    data = obj_in.dict(exclude_unset=True)
    for field, value in data.items():
        setattr(db_subtask, field, value)
    db.commit()
    db.refresh(db_subtask)
    return db_subtask


def delete_subtask(db: Session, subtask_id: int) -> bool:
    db_subtask = get_subtask(db, subtask_id)
    if not db_subtask:
        return False
    db.delete(db_subtask)
    db.commit()
    return True
```