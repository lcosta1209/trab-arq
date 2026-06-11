from abc import ABC, abstractmethod
from core.domain.task import Task, TaskStatus


class TaskRepository(ABC):
    """Port de saída: contrato para persistência de tarefas."""

    @abstractmethod
    def find_by_id(self, task_id: int) -> Task | None:
        pass

    @abstractmethod
    def save(self, task: Task) -> Task:
        pass

    @abstractmethod
    def list_all(self) -> list[Task]:
        pass


class EventPublisher(ABC):
    """Port de saída: contrato para publicação de eventos."""

    @abstractmethod
    def publish(self, event_name: str, payload: dict) -> None:
        pass


# INPUT PORT 

class TaskService:

    def __init__(self, repository: TaskRepository, publisher: EventPublisher):
        self.repository = repository
        self.publisher = publisher

    def list_tasks(self) -> list[Task]:
        return self.repository.list_all()

    def create_task(self, title: str) -> Task:
        task = Task(id=0, title=title, status=TaskStatus.PENDING, created_at=__import__("datetime").datetime.now())
        return self.repository.save(task)

    def update_status(self, task_id: int, new_status: TaskStatus) -> Task:
        task = self.repository.find_by_id(task_id)
        if task is None:
            raise ValueError(f"Tarefa {task_id} não encontrada.")

        updated = task.update_status(new_status)
        saved = self.repository.save(updated)

        # EDA: publica evento quando tarefa é concluída
        if saved.is_done():
            self.publisher.publish("task.completed", {"task_id": saved.id, "title": saved.title})

        return saved
