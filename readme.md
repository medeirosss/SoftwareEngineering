# TaskFlow – Projeto Ágil no GitHub (TechFlow Solutions)
##v1

## Objetivo
Este repositório simula o desenvolvimento de um sistema web básico de gerenciamento de tarefas para uma startup de logística, permitindo acompanhar o fluxo de trabalho em tempo real, priorizar tarefas e registrar progresso.

## Escopo inicial
- CRUD de tarefas (Create, Read, Update, Delete)
- Campos principais: título, descrição, status (todo / in_progress / done)
- API HTTP simples (Flask)
- Persistência local com SQLite (para fins didáticos)

## Metodologia adotada
Kanban no GitHub Projects, com colunas:
- To Do
- In Progress
- Done

## Como executar (local)
1. Criar ambiente:
   - `python -m venv .venv`
   - Ativar a venv
2. Instalar dependências:
   - `pip install -r requirements.txt`
3. Rodar aplicação:
   - `python -m src.app`
4. Testar:
   - `pytest -q`

## Controle de Qualidade (GitHub Actions)
O pipeline CI executa automaticamente os testes com pytest em push/pull request.

## Gestão de Mudanças (mudança de escopo simulada)
### O que mudou?
Foi adicionada a necessidade de filtrar tarefas por status na listagem (ex.: listar apenas `done`).

### Por que mudou?
Durante a validação com stakeholders, percebeu-se que a equipe precisava de uma visão rápida por status para priorização operacional e acompanhamento de tarefas concluídas.

### Onde está implementado?
- Endpoint: `GET /tasks?status=done`
- Card criado no Kanban
- Commit específico implementando a alteração
