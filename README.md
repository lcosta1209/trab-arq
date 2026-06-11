# TaskFlow – Gerenciador de Tarefas

**Grupo:** Juliano Rehling, Lucas Costa, Renan Chaves e André Henssler  
**Arquitetura:** Hexagonal (Ports & Adapters) + EDA + Monolito

---

## Estrutura do Projeto

```
taskflow/
├── core/
│   ├── domain/
│   │   └── task.py           # Entidade Task e enum TaskStatus
│   └── ports/
│       └── task_service.py   # Casos de uso + interfaces (ports)
├── adapters/
│   ├── http/
│   │   └── task_router.py    # Adapter de entrada: API REST (FastAPI)
│   ├── db/
│   │   └── postgres_repository.py  # Adapter de saída: PostgreSQL
│   └── events/
│       └── log_publisher.py  # Adapter de saída: publicador de eventos
├── infrastructure/
│   └── database.py           # Conexão e migrations do banco
├── main.py                   # Ponto de entrada + injeção de dependências
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

---

## Arquitetura Hexagonal

```
         [HTTP Request]
               ↓
     ┌─────────────────┐
     │  Adapter: HTTP  │  ← Adapter de ENTRADA
     └────────┬────────┘
              ↓
     ┌─────────────────┐
     │   TaskService   │  ← CORE (regras de negócio)
     │   (use cases)   │    Não conhece FastAPI nem PostgreSQL
     └────────┬────────┘
              ↓
     ┌────────┴──────────────┐
     ↓                       ↓
┌──────────┐         ┌──────────────┐
│ Postgres │         │ LogPublisher │  ← Adapters de SAÍDA
│ Repo     │         │ (Evento EDA) │
└──────────┘         └──────────────┘
```

A regra principal da arquitetura hexagonal:
> **O core nunca importa nada dos adapters.** Os adapters é que implementam as interfaces (ports) do core.

---

## EDA – Event-Driven Architecture

Quando uma tarefa tem o status atualizado para `done`, o `TaskService` publica automaticamente um evento `task.completed` via `EventPublisher`.

O `LogEventPublisher` é a implementação mínima (loga no console). Para expandir, basta criar um novo adapter implementando a mesma interface — ex: `RabbitMQPublisher`.

---

## Endpoints

| Método | Rota                     | Descrição               |
|--------|--------------------------|-------------------------|
| GET    | `/tasks/`                | Lista todas as tarefas  |
| POST   | `/tasks/`                | Cria uma nova tarefa    |
| PATCH  | `/tasks/{id}/status`     | Atualiza o status       |
| GET    | `/health`                | Health check            |

### Status disponíveis
- `pending` – Pendente
- `in_progress` – Em andamento
- `done` – Concluído

---

## Como rodar

### Com Docker (recomendado)
```bash
docker-compose up --build
```

### Sem Docker
```bash
pip install -r requirements.txt

# Configure as variáveis de ambiente do banco:
export DB_HOST=localhost
export DB_PORT=5432
export DB_NAME=taskflow
export DB_USER=postgres
export DB_PASSWORD=postgres

uvicorn main:app --reload
```

Acesse a documentação interativa em: **http://localhost:8000/docs**

---

## O que falta implementar

- [ ] Autenticação (JWT ou sessão)
- [ ] Deletar tarefas
- [ ] Filtrar tarefas por status
- [ ] Substituir `LogEventPublisher` por RabbitMQ/Kafka
- [ ] Testes unitários do core (sem dependências externas)
- [ ] Frontend Kanban
