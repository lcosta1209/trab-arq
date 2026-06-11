import os
import psycopg2

def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", 5432),
        dbname=os.getenv("DB_NAME", "taskflow"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "postgres"),
    )

def run_migrations(conn):
    """Cria a tabela de tarefas se não existir."""
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id         SERIAL PRIMARY KEY,
                title      VARCHAR(255) NOT NULL,
                status     VARCHAR(50)  NOT NULL DEFAULT 'pending',
                created_at TIMESTAMP    NOT NULL DEFAULT NOW()
            );
        """)
        conn.commit()
