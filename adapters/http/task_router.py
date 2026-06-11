from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from core.domain.task import TaskStatus
from core.ports.task_service import TaskService

router = APIRouter(prefix="/tasks", tags=["tasks"])

# Injetado via main.py
_service: TaskService = None

def set_service(service: TaskService):
    global _service
    _service = service


# ---------- Schemas ----------

class CreateTaskRequest(BaseModel):
    title: str

class UpdateStatusRequest(BaseModel):
    status: TaskStatus

class TaskResponse(BaseModel):
    id: int
    title: str
    status: TaskStatus
    created_at: str


# ---------- Endpoints ----------

@router.get("/", response_model=list[TaskResponse])
def list_tasks():
    tasks = _service.list_tasks()
    return [_to_response(t) for t in tasks]


@router.post("/", response_model=TaskResponse, status_code=201)
def create_task(body: CreateTaskRequest):
    task = _service.create_task(body.title)
    return _to_response(task)


@router.patch("/{task_id}/status", response_model=TaskResponse)
def update_status(task_id: int, body: UpdateStatusRequest):
    try:
        task = _service.update_status(task_id, body.status)
        return _to_response(task)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


def _to_response(task) -> TaskResponse:
    return TaskResponse(
        id=task.id,
        title=task.title,
        status=task.status,
        created_at=task.created_at.isoformat(),
    )
