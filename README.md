# TaskFlow — Sistema de Gerenciamento de Tarefas

Aplicação web desenvolvida em Python com Flask para cadastro de usuários e gerenciamento colaborativo de tarefas. O projeto implementa autenticação, operações CRUD, atribuição de responsáveis, filtros por status e um dashboard do grupo.

## Funcionalidades

- Cadastro, login e logout de usuários;
- senhas protegidas com hash;
- criação, visualização, edição e exclusão de tarefas;
- atribuição de tarefas a usuários cadastrados;
- status `Pendente`, `Em andamento` e `Concluída`;
- filtro de tarefas por status;
- dashboard com totais e atualizações recentes;
- controle de permissões;
- interface responsiva com Bootstrap;
- persistência em banco de dados SQLite;
- testes automatizados com Pytest.

## Regras de acesso

- É necessário estar autenticado para acessar o sistema.
- Todos os usuários autenticados podem visualizar o dashboard e as tarefas do grupo.
- O criador e o responsável atribuído podem editar uma tarefa.
- Somente o criador pode excluir a tarefa.

## Tecnologias

- Python 3.11 ou superior;
- Flask;
- Flask-SQLAlchemy;
- Flask-Login;
- Flask-WTF;
- SQLite;
- HTML, CSS e Bootstrap 5;
- Pytest.

## Instalação no Windows

Abra o PowerShell dentro da pasta do projeto e execute:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python run.py
```

Caso o PowerShell bloqueie a ativação, execute antes:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

## Instalação no Linux ou macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python run.py
```

Depois, acesse `http://127.0.0.1:5000` no navegador. O banco SQLite é criado automaticamente no primeiro uso, dentro da pasta `instance`.

## Executar os testes

Com o ambiente virtual ativado:

```bash
pytest -v
```

## Estrutura do projeto

```text
taskflow/
├── app/
│   ├── auth/              # Cadastro, login e logout
│   ├── main/              # Dashboard
│   ├── tasks/             # CRUD e filtros de tarefas
│   ├── static/css/        # Estilos da aplicação
│   ├── templates/         # Páginas HTML
│   ├── extensions.py      # Extensões do Flask
│   └── models.py          # Modelos do banco de dados
├── tests/                 # Testes automatizados
├── .gitignore
├── requirements.txt
├── run.py
└── README.md
```

## Publicar no GitHub

Antes da entrega, remova dados de teste que não devam ser publicados. A pasta `instance`, que contém o banco local, já está ignorada pelo Git.

```bash
git init
git add .
git commit -m "Implementa sistema de gerenciamento de tarefas"
git branch -M main
git remote add origin URL_DO_SEU_REPOSITORIO
git push -u origin main
```

Substitua `URL_DO_SEU_REPOSITORIO` pelo endereço informado pelo GitHub. Não faça commits depois do prazo final estabelecido pelo professor.

## Autores

Adicione aqui o nome completo e o RA dos integrantes antes da entrega.
