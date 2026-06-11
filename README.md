TaskFlow

Gerenciador de tarefas estilo Kanban desenvolvido como trabalho acadêmico para a disciplina de Arquitetura de Software.

Grupo: Juliano Rehling, Lucas Costa, Renan Chaves e André Henssler


Sobre o projeto

O sistema permite criar tarefas e mover elas entre três status: Pendente, Em andamento e Concluído. Quando uma tarefa é concluída, um evento é disparado automaticamente — é aqui que entra o EDA.

A arquitetura escolhida foi a Hexagonal (Ports & Adapters) rodando como monolito. A ideia principal é manter o core da aplicação completamente isolado de frameworks e banco de dados — o FastAPI e o PostgreSQL são detalhes de infraestrutura, não o centro do sistema.


Estrutura

taskflow/
├── core/
│   ├── domain/
│   │   └── task.py                    # Entidade Task e enum de status
│   └── ports/
│       └── task_service.py            # Casos de uso e interfaces
├── adapters/
│   ├── http/
│   │   └── task_router.py             # Entrada via API REST
│   ├── db/
│   │   └── postgres_repository.py     # Persistência no PostgreSQL
│   └── events/
│       └── log_publisher.py           # Publicação de eventos
├── infrastructure/
│   └── database.py                    # Conexão e criação da tabela
├── main.py                            # Injeção de dependências e inicialização
├── Dockerfile
├── docker-compose.yml
└── requirements.txt


Como a arquitetura funciona na prática

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
│   Repo   │         │ (Evento EDA) │
└──────────┘         └──────────────┘

A regra que guia tudo: o core não importa nada dos adapters. São os adapters que implementam as interfaces definidas pelo core, nunca o contrário.


Endpoints

MétodoRotaDescriçãoGET/tasks/Lista todas as tarefasPOST/tasks/Cria uma nova tarefaPATCH/tasks/{id}/statusAtualiza o statusGET/healthHealth check

Status aceitos: pending, in_progress, done


Como rodar

bashdocker-compose up --build

A documentação interativa fica disponível em http://localhost:8000/docs.

Sem Docker, é necessário configurar as variáveis de ambiente do banco (DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD) e rodar uvicorn main:app --reload dentro da pasta do projeto.


O que ainda falta


Autenticação
Deletar tarefas
Filtrar por status
Testes unitários do core
Frontend Kanban