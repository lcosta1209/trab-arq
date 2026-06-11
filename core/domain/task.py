from enum import Enum
from dataclasses import dataclass
from datetime import datetime


class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    DONE = "done"


@dataclass
class Task:
    id: int
    title: str
    status: TaskStatus
    created_at: datetime

    def update_status(self, new_status: TaskStatus) -> "Task":
        return Task(
            id=self.id,
            title=self.title,
            status=new_status,
            created_at=self.created_at,
        )

    def is_done(self) -> bool:
        return self.status == TaskStatus.DONE
