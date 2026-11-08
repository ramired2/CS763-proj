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