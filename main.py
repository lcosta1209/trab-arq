from fastapi import FastAPI
from infrastructure.database import get_connection, run_migrations
from adapters.db.postgres_repository import PostgresTaskRepository
from adapters.events.log_publisher import LogEventPublisher
from adapters.http.task_router import router as task_router, set_service
from core.ports.task_service import TaskService

app = FastAPI(title="TaskFlow API")

# ---------- Composição das dependências (Dependency Injection manual) ----------
conn = get_connection()
run_migrations(conn)

repository = PostgresTaskRepository(conn)
publisher  = LogEventPublisher()
service    = TaskService(repository, publisher)

set_service(service)

# ---------- Rotas ----------
app.include_router(task_router)


@app.get("/health")
def health():
    return {"status": "ok"}
