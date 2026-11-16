# Functional Peer Review and Evaluation Gateway

## AI Usage Log
| AI Contribution % | Summary of prompt |
| :---------------: | ----------------- |
|       100%        | Using ProjectPortalDomainServices to create the functional codebase w nine specific test cases and using postgresql |

This FastAPI implementation follows the Domain 3 functional requirements and
REST endpoints in the provided `ProjectPortalDomainServices` document. It
stores its state in PostgreSQL as a JSONB document, initialized with sample
projects, scoped rubrics, and reviews when the database is first used.

Configure `DATABASE_URL` with a PostgreSQL connection string, then run the API
from this directory:

```sh
python -m pip install -r requirements.txt
export DATABASE_URL=postgresql://eval_gateway:password@localhost:5432/eval_gateway
uvicorn app.main:app --reload
```

For a local PostgreSQL instance, from the repository root run
`docker compose up --build`; the app is available at `http://localhost:8000`.
Set `POSTGRES_PASSWORD` before starting Compose. The sample password fallback
is for local development only and must not be used in production.

Run the functional tests:

```sh
python -m pip install -r requirements.txt httpx pytest
python -m pytest -q
```

The API documentation is available at `/docs`. The seeded sample data is stored
in PostgreSQL and persists between process restarts. Each request locks and
updates the single JSONB state document to avoid lost updates; this keeps the
functional prototype simple but serializes requests. A production deployment
with higher throughput should move the data into normalized relational tables.
Peer reviews do not expose reviewer identity. Rubric changes and deletion are
rejected while any project is bound to that rubric.
