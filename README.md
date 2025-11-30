tutor_system/
├── app/
│   ├── integration/         # Layer: Integration (Adapters for SSO, Library, DataCore)
│   ├── repositories/        # Layer: Data Access (CRUD operations)
│   ├── domain/              # Layer: Business/Domain (Pure business logic/rules)
│   ├── services/            # Layer: Application/Service (Orchestration)
│   ├── routers/             # Layer: User Interface (API Endpoints & View Controllers)
│   ├── models.py            # Database Entities (SQLAlchemy)
│   ├── database.py          # Database Connection
│   ├── main.py              # App Entry Point
│   └── templates/           # HTML Views (Jinja2)
├── requirements.txt
└── README.md

# Create enviroment

`python -m venv venv`
`venv\Scripts\activate`
# Install requirements

`pip install -r requirements.txt`

# Run

First you need to run the script.sql to hard code database (Mysql : 3306)

`uvicorn app.main:app --reload --port 8000`