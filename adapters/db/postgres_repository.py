import psycopg2
from datetime import datetime
from core.domain.task import Task, TaskStatus
from core.ports.task_service import TaskRepository

class PostgresTaskRepository(TaskRepository):
    """Adapter de saída: implementação do repositório usando  PostgreSQL."""

    def __init__(self, conn):
        self.conn = conn

    def find_by_id(self, task_id: int) -> Task | None:
        with self.conn.cursor() as cur:
            cur.execute("SELECT id, title, status, created_at FROM tasks WHERE id = %s", (task_id,))
            row = cur.fetchone()
            return self._to_entity(row) if row else None

    def save(self, task: Task) -> Task:
        with self.conn.cursor() as cur:
            if task.id == 0:
                cur.execute(
                    "INSERT INTO tasks (title, status, created_at) VALUES (%s, %s, %s) RETURNING id, title, status, created_at",
                    (task.title, task.status.value, datetime.now()),
                )
            else:
                cur.execute(
                    "UPDATE tasks SET status = %s WHERE id = %s RETURNING id, title, status, created_at",
                    (task.status.value, task.id),
                )
            self.conn.commit()
            return self._to_entity(cur.fetchone())

    def list_all(self) -> list[Task]:
        with self.conn.cursor() as cur:
            cur.execute("SELECT id, title, status, created_at FROM tasks ORDER BY id")
            return [self._to_entity(row) for row in cur.fetchall()]

    def _to_entity(self, row) -> Task:
        return Task(id=row[0], title=row[1], status=TaskStatus(row[2]), created_at=row[3])
