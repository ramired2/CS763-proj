# Functional Peer Review and Evaluation Gateway

## AI Usage Log
| AI Contribution % | Summary of prompt |
| :---------------: | ----------------- |
|       100%        | Using ProjectPortalDomainServices to create the functional codebase w nine specific test cases |

This self-contained FastAPI implementation follows the Domain 3 functional
requirements and REST endpoints in the provided `ProjectPortalDomainServices`
document. It includes in-memory sample projects, scoped rubrics, reviews, and
nine happy-path tests.

Run the API from this directory:

```sh
python -m pip install -r ../requirements.txt
uvicorn app.main:app --reload
```

Run the functional tests:

```sh
python -m pip install httpx pytest
python -m pytest -q
```

The API documentation is available at `/docs`. The sample data is in memory
and resets when the process restarts. Peer reviews do not expose reviewer
identity. Rubric changes and deletion are rejected while any project is bound
to that rubric.
