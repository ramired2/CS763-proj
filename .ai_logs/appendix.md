# AI Prompt Appendix

## Prompts and response descriptions

### 5:14 PM — Add SonarQube to the DevSecOps workflow

**Prompt**

> outline the general steps i need to do in order to add sonarqube to my devsecops file

**Response description**

Outlined creating/importing a Sonar project, storing a token in GitHub Actions Secrets, configuring scanner environment variables and project properties, fetching full Git history, optionally importing Python coverage, choosing whether the Quality Gate blocks CI, and verifying a workflow run.

### 5:29 PM — Sonar project properties

**Prompt**

> What information is needed in the sonar.project.properties file and where should I have it

**Response description**

Corrected the conventional filename to `sonar-project.properties`, recommended putting it in the repository root, and listed project key, organization, source/test paths, encoding, and Python version as analysis configuration rather than secrets.

**Suggested example**

```properties
sonar.projectKey=YOUR_SONARCLOUD_PROJECT_KEY
sonar.organization=YOUR_SONARCLOUD_ORGANIZATION_KEY
sonar.sources=app
sonar.tests=tests
sonar.sourceEncoding=UTF-8
sonar.python.version=3.12

# Optional; use after generating coverage.xml with pytest-cov.
# sonar.python.coverage.reportPaths=coverage.xml
```

### 5:43 PM — Check SonarQube setup

**Prompt**

> Check that I have correctly set up scanning with SonarQube

**Response description**

Inspected the workflow and noted that it passed the token but did not yet provide the self-hosted server URL; no `sonar-project.properties` file was present at that point. Recommended project properties and full checkout history.

### 5:46 PM — Clarify SonarQube Cloud usage

**Prompt**

> I have already set up the SONAR_TOKEN as secret key as a GitHub Actions secret and am using SonarQube cloud for this

**Response description**

Clarified that SonarQube Cloud does not need `SONAR_HOST_URL`; the token setup was already correct. Recommended adding the exact Cloud project and organization keys in a root `sonar-project.properties` file and moving `fetch-depth: 0` to checkout in the scan job.

### 5:50 PM — Purpose of project properties

**Prompt**

> if i am not adding my secrets to the sonar-project.properties file, then what is its purpose

**Response description**

Explained that the properties file supplies project identity and analysis scope (for example, source and test directories), while the token is separately provided through GitHub Actions Secrets.

**Suggested SonarQube Cloud properties**

```properties
sonar.projectKey=YOUR_PROJECT_KEY
sonar.organization=YOUR_ORGANIZATION_KEY
sonar.sources=app
sonar.tests=tests
sonar.sourceEncoding=UTF-8
sonar.python.version=3.12
```

### 5:50 PM — Meaning of the project-key placeholder

**Prompt**

> So does the "YOUR_PROJECT_KEY" not matter? is this a temporary placeholder?

**Response description**

Confirmed that `YOUR_PROJECT_KEY` and `YOUR_ORGANIZATION_KEY` are placeholders that must be replaced with the exact values from SonarQube Cloud; they are not credentials.

### 5:51 PM — Meaning and source of `projectKey`

**Prompt**

> what is a projectKey? is this a random value or is it from SonarQube?

**Response description**

Explained that the project key uniquely identifies a project in SonarQube Cloud and should be copied from project information/settings or obtained during project creation/import.

### 5:59 PM — Review the properties file

**Prompt**

> does this file look correct?

**Response description**

Reviewed `sonar-projects.properties`. The properties and paths looked structurally appropriate, but the filename was pluralized incorrectly. Recommended renaming it to `sonar-project.properties` and verifying the project and organization keys in SonarQube Cloud.

## Functional Codebase and SonarQube Follow-up

### November 10 — Create a functional codebase and tests

**Prompt**

> create ‘functional-codebase/’ with the provided test cases
>
> `functional-codebase/` will contain raw and unmitigated source code that follows the functional requirements from `ProjectPortalServices.pdf`. The requirements will be achieved with REST APIs. Implement happy paths for retrieving a submitted evaluation, submitting an individual evaluation, editing/deleting an unused rubric, creating an evaluation schema, retrieving a project summary and a specific project review, and editing/removing a specific project review.

**Response**

Created a standalone FastAPI service, seeded in-memory project/rubric/review data, and nine tests. The implementation uses project-scoped reviews and rubric-scoped criteria and reports faculty and anonymous peer review results separately.

**Representative API and test snippets**

```python
API_PREFIX = "/api/v1/evaluations"

@app.get(f"{API_PREFIX}/projects/{{project_id}}/summary")
def project_summary(project_id: str, request: Request) -> dict[str, Any]:
    ...
```

```python
response = client.post(
    f"{API_PREFIX}/projects/project-101/reviews",
    json={"reviewer_role": "student_peer", "scores": [...]},
)
assert response.status_code == 201
```

### November 10 — Use only the provided PDF

**Prompt**

> Do not use spec.md at all, use only the ProjectPortalDomainServices file that was provided

**Response**

Read `ProjectPortalDomainServices.pdf` directly and revised the implementation to use its Domain 3 REST routes and requirements: rubric scopes by project/course/lab, one governing rubric per project, separate faculty and anonymous peer reviews, aggregated reports, and query filters. The generated routes use the PDF's `/api/v1/evaluations/` prefix.

### November 10 — Fix the `API_PREFIX` import error

**Prompt**

> I am getting the following error in my devsecops " ImportError: cannot import name 'API_PREFIX' from 'app.main'" from line 17, how can I fix this

**Response**

Explained that running pytest from the repository root imports the root `app/main.py`, while the functional tests target the separate `functional-codebase/app` package. Recommended running pytest after changing into that subdirectory, or changing the CI test step:

```yaml
- name: Run tests
  run: cd functional-codebase && python -m pytest -q
```

### November 10 — Determine Semgrep's scan target

**Prompt**

> In 50 words state whether cd functional-codebase && semgrep scan --config p/python app tests will scan the tests from functional-codebase/tests or not

**Response**

Confirmed that, after changing directory, `app` and `tests` resolve under `functional-codebase`; Semgrep scans supported, non-ignored files there, including `test_api.py`, and does not also scan root-level `tests`.

### November 10 — Disable SonarQube shallow clone

**Prompt**

> I am getting a warning message to disable "shallow clone" from sonarqube, explain to me in 200 words or less how I can do this?

**Response**

Recommended setting `fetch-depth: 0` on the checkout action in the same job as the SonarQube scan, so the scanner receives full Git history:

```yaml
- name: Check out source
  uses: actions/checkout@...
  with:
    fetch-depth: 0
```

### November 10 — Explain why only `app/main.py` is scanned

**Prompt**

> Explain in 200 words or less why SonarQube is only scanning app/main.py

**Response**

Pointed out that the root `sonar-project.properties` had `sonar.sources=app` and `sonar.tests=tests`, so the workflow scanned the root `app/` directory, which contained only `main.py`, rather than the separate functional codebase. To scan the latter, configure:

```properties
sonar.sources=functional-codebase/app
sonar.tests=functional-codebase/tests
```

### November 10 — Export prompts and responses to this appendix

**Prompt**

> Export each prompt and your responses along with snippets of the code and append it to appendix.md

**Response**

Appended this conversation's functional-codebase and SonarQube prompts and response summaries to this appendix, with representative code and CI configuration snippets.