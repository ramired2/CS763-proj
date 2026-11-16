# MASTER CONCEPTUAL JOURNAL & AI TELEMETRY LOG
## AI Usage Log
| AI Contribution % | Summary of prompt   |
| :---------------: | ------------------- |
|        5%         | explaining how to identify how an HTTP request payload is captured, explaining/confirming if main.py followed singleton approach or repository.  |

* **Student Name:** Daisy Ramirez
* **Assigned Domain Module:** Domain 3: The Peer Review & Evaluation Gateway
* **Core Technology Stack:** Python/FastAPI

\================================================================================

## SECTION 1: SYSTEM ENVIRONMENT & TOOL SPECIFICATION

\================================================================================

### 1.1 AI Tool & Engine Deployments

*Identify all autonomous developer agents, conversational LLMs, inline assistants, or documentation tools utilized during this project milestone.*

| Tool Context        | Framework / Platform Name & Version | Underlying LLM Brain Model String     | Operational Setting / Access Mode     |
| :------------------ | :---------------------------------- | :------------------------------------ | :------------------------------------ |
| **Code Generation** | VS Copilot                          | Copilot Fusion (standard)/ GPT-6 Luna | Local Sandboxed Docker Container      |

### 1.2 Verification Telemetry Access Checklist

- [x] Primary Auto-Extracted Session Logs / Appendices Saved to `/.ai_logs/` directory

\================================================================================

## SECTION 2: COGNITIVE REFLECTION — CODE GENERATION & COMPREHENSION

\================================================================================

### 2.1 The Architectural Flow (How You Understand the Code)

> Given the prompt along with the master spec I gave Copilot Fusion, it generated 
7 main routes
* /health
* /rubrics (POST GET)
* /rubrics/{{rubric_id}} (GET/PUT/DELETE)
* /projects/{{project_id}}/summary (GET)
* /projects/{{project_id}}/reviews (POST/ GET)
* /projects/{{project_id}}/reviews/{{review_id}} (GET/ PUT/ DELETE)
* /reports

In terms of how a HTTP request payload is captured by the framework, 
for creating rubrics, specifically, it will take the HTTPs request and validate 
the data store for the request. Once it has been validated, 
the body will contain 
the input for creating a rubric in JSON. It will then parse out information 
like name, description, scope_type, and scope_id of the rubric. At the mpment the API
 service uses a JSONB to initialize information into the database. Afterwards, 
 any CRUD changes would be made directly on the dictionaries, not yet on the database.
 The other main routes will have a similar process, they will mainly differ in the 
 type of information passed in the body. 

Looking at the code that was produced by Copilot, it appears that it did not 
fully stick to a single design pattern. It seems to have done a mix of different 
design patterns, although from MVC, Repository, or Singleton, it would 
mostly closely resemble Singleton. That being said, there is not as many similarities 
as there are multiple classes being used in 
addition to the fact that there are new connections being opened that then load the sample data.

### 2.2 Defensive Edge-Case Evaluation (Line-by-Line Code Review)
#### main.py (imports were not included)
> ```TEMP```
EXPLAIN







### 2.3 The AI Agent's "Security Sins" (Evaluating Code Deficiencies)
> 

\================================================================================

## SECTION 3: COGNITIVE REFLECTION — DOCUMENT AUTHORING & THREAT DESIGN

\================================================================================

### 3.1 AI Collaboration Matrix for Security Analysis

> AI was used to list different types of information that should be used to make 
these security requirements. It gave me examples of different categories and a brief 
sentence explaining what that category entails. Otherwise, no AI was used for creating 
the abuse cases, attack trees, and threat modeling frameworks.

### 3.2 Evaluation of Automated Conceptual "Blind Spots"
> From the prompt I asked Copilot, it did not hallucinate anything or overreach with 
my ask. 

\================================================================================

## SECTION 4: HUMAN VERIFICATION & AUDIT TRAIL LOG

\================================================================================ *Record every manual configuration test, integration check, dynamic execution verification (Postman, cURL loops), or tool scan triage loop handled completely by you by hand.*

| Timestamp        | Component Target       | Testing/Auditing New Methodology                                           | Verified Outcome / Discovered Defect                                                                                                                   |
| :--------------- | :--------------------- | :------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------- |
| *\[2026-11-10\]* | *`test_api.py`*        | *Testing if the tests passed as it failed in devsecops but passed locally* | Passed locally and failed in devsecops x4. UTC was deprecated and would work locally but UTC did not exist in DateTime when the devsecops installed it |
| *\[2026-11-10\]* | *`sast-triage-report`* | *Testing Semgrep output stream as it identified 0 findings*                | Attempted python tag p/python. There was no error.                                                                                                     |
| *\[2026-11-10\]* | *`sast-triage-report`* | *Testing Semgrep output stream as it identified 0 findings*                | Attempted python tag p/owasp-top-ten. There was no error.                                                                                              |
| *\[2026-11-10\]* | *`sast-triage-report`* | *Testing Semgrep output stream as it identified 0 findings*                | Attempted python tag p/security-audit. There was no error.                                                                                             |
| *\[2026-11-15\]* | *`Dockerfile`*         | *Testing app would run in container after modifying structure*             | App was not running in container 3x. I missed identifying to use functional-codebase for the app in the Dockerfile                                     |

&nbsp;