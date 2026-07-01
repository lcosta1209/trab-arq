TaskFlow

Gerenciador de tarefas estilo Kanban desenvolvido como trabalho acadêmico para a disciplina de Arquitetura de Software.

Grupo: Juliano Rehling, Lucas Costa, Renan Chaves e André Henssler


Sobre o projeto

O sistema permite criar tarefas e mover elas entre três status: Pendente, Em andamento e Concluído. Quando uma tarefa é concluída, um evento é disparado automaticamente — é aqui que entra o EDA.

A arquitetura escolhida foi a Hexagonal (Ports & Adapters) rodando como monolito. A ideia principal é manter o core da aplicação completamente isolado de frameworks e banco de dados — o FastAPI e o PostgreSQL são detalhes de infraestrutura, não o centro do sistema.
