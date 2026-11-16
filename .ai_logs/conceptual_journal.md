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
```
# set prefix for API
API_PREFIX = "/api/v1/evaluations"
# used for DB table
STATE_TABLE = "evaluation_gateway_state"
# used for locking when loading DB
STATE_LOCK_ID = 7632026
# different types of acceptable user types
ReviewRole = Literal["faculty_instructor", "student_peer"]
# different types of scopes for projects
ScopeType = Literal["project", "course", "lab"]
# acces logging functionality
logger = logging.getLogger(__name__)
```

```
# Creates new IDs but there needs to be a check that the ID does not curently 
# exist.
def new_id() -> str:
    return str(uuid4())
```

```
# Returns a timestamp which is used for creating/editing purposes. Many systems do 
# use UTC so it is good to maintain this standard. There are no checks needed
def now_utc() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")
```

```
# Creates a class Criterion that uses a name, description, weight, and max points.
# It ensures that the weight is between 0 and 1 and that the max_amount of points
# is above 0. It does not set an upper boundary. Once data is being stored in 
# the database it would be a good idea to add criterion IDs as criterion would likely 
# have its own relational table. Although, in its current set up criterion IDs are 
# created when a rubric is created.
class Criterion(BaseModel):
    name: str
    description: str
    weight: float = Field(gt=0, le=1) # 0<= weight <= 1
    max_points: float = Field(gt=0)   # max_points >= 0

```

```
# Creates a class RubricCreate that takes in the name of the rubric, a description
# the scope_type ("project", "course", "lab"), scope_id, and the criteria where there must be 
# at least one criteria. It then validates that the weights for the criteria summed up 
# equal to 1. Otherwise, it raises an error. It would be a good idea to add in the ID for 
# the rubric being created which would be used in a relational table. At the moment, IDs are 
# created and stored when a rubric is created. 
class RubricCreate(BaseModel):
    name: str
    description: str = ""
    scope_type: ScopeType
    scope_id: str
    criteria: list[Criterion] = Field(min_length=1)

    # makes sure criteria weights sum to 1
    @model_validator(mode="after")
    def weights_total_one(self) -> RubricCreate:
        # otherwise raise an error the sum is not equal to 1
        if not isclose(sum(item.weight for item in self.criteria), 1.0):
            raise ValueError("Criterion weights must sum to 1")
        return self

```

```
# Creates a class RubricUpdate that has a name, description, criteria and checks that 
# the weight of the criteria equal to one. Criterion already has restrictions 
# to ensure that its weights are between 0 and 1, so the only check needed here is 
# that the sums all equal to one.
class RubricUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    criteria: list[Criterion] | None = Field(default=None, min_length=1)

    @model_validator(mode="after")
    def weights_total_one(self) -> RubricUpdate:
        if self.criteria is not None and not isclose(
            sum(item.weight for item in self.criteria), 1.0
        ):
            raise ValueError("Criterion weights must sum to 1")
        return self

```

```
# Class ScoreInput that takes in the criterion ID, the score that is greater than 
# or equal to or greater than zero, and the feedback. It would be a good idea to set 
# some restriction for feedback length so that there is more context for the scores.
class ScoreInput(BaseModel):
    criterion_id: str
    score: float = Field(ge=0)
    feedback: str

```

```
# Create a class ReviewCreate that creates a review setting if the reviewer is 
# a student_peer or faculty_instructor along with their reviews. It further
# sets a minimum of one score input needed 
class ReviewCreate(BaseModel):
    reviewer_role: ReviewRole
    scores: list[ScoreInput] = Field(min_length=1)

```

```
# Create a class ReviewUpdate that is used for updating the review role (student_peer, facilitator_instructor)
# and the input scores
class ReviewUpdate(BaseModel):
    reviewer_role: ReviewRole | None = None
    scores: list[ScoreInput] | None = Field(default=None, min_length=1)

```

```
# a store of mocks data that contains criteria for a rubric, a rurbic, and reviews
# in a dictionary 
def create_store() -> dict[str, Any]:
    criteria = [
        {
            "criterion_id": "criterion-analysis",
            "name": "Analysis",
            "description": "Strength and clarity of analysis.",
            "weight": 0.6,
            "max_points": 5.0,
        },
        {
            "criterion_id": "criterion-design",
            "name": "Design",
            "description": "Quality of the proposed design.",
            "weight": 0.4,
            "max_points": 5.0,
        },
    ]
    return {
        "courses": ["CS501", "CS502", "CS503"],
        "labs": ["lab-cybersec", "lab-systems", "lab-unused"],
        "projects": {
            "project-101": {
                "project_id": "project-101",
                "course_id": "CS501",
                "lab_id": "lab-cybersec",
                "rubric_id": "rubric-101",
            },
            "project-102": {
                "project_id": "project-102",
                "course_id": "CS501",
                "lab_id": "lab-cybersec",
                "rubric_id": "rubric-101",
            },
        },
        "rubrics": {
            "rubric-101": {
                "rubric_id": "rubric-101",
                "name": "Research Project Rubric",
                "description": "Evaluate research project performance.",
                "scope_type": "course",
                "scope_id": "CS501",
                "created_at": "2026-09-05T16:00:00Z",
                "updated_at": "2026-09-05T16:00:00Z",
                "criteria": criteria,
            },
            "rubric-102": {
                "rubric_id": "rubric-102",
                "name": "Unused Project Rubric",
                "description": "Not currently bound to a project.",
                "scope_type": "lab",
                "scope_id": "lab-unused",
                "created_at": "2026-09-06T16:00:00Z",
                "updated_at": "2026-09-06T16:00:00Z",
                "criteria": criteria,
            },
        },
        "reviews": {
            "review-101": {
                "review_id": "review-101",
                "project_id": "project-101",
                "reviewer_role": "faculty_instructor",
                "submitted_at": "2026-10-08T17:00:00Z",
                "scores": [
                    {
                        "criterion_id": "criterion-analysis",
                        "score": 4,
                        "feedback": "The analysis is clear and well supported.",
                    },
                    {
                        "criterion_id": "criterion-design",
                        "score": 5,
                        "feedback": "The design addresses the project goals.",
                    },
                ],
            },
            "review-102": {
                "review_id": "review-102",
                "project_id": "project-101",
                "reviewer_role": "student_peer",
                "submitted_at": "2026-10-09T14:30:00Z",
                "scores": [
                    {
                        "criterion_id": "criterion-analysis",
                        "score": 5,
                        "feedback": "The reasoning is easy to follow.",
                    },
                    {
                        "criterion_id": "criterion-design",
                        "score": 4,
                        "feedback": "The design could use more detail.",
                    },
                ],
            },
        },
    }
```

```
# Sets the version and title and instantiates the app 
app = FastAPI(title="Peer Review and Evaluation Gateway", version="1.0.0")
```

```
# loads the JSONB store information into the database
def load_database_state(database_url: str) -> tuple[Connection, dict[str, Any]]:
    """Open a transaction and load the shared JSONB state document."""

    # makes the connection to the DB
    connection = connect(database_url, row_factory=dict_row)

    try:
        # run the query to make the table form the store data if it is not already existin
        # each new instance will open a new connection
        connection.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {STATE_TABLE} (
                state_id SMALLINT PRIMARY KEY CHECK (state_id = 1),
                payload JSONB NOT NULL
            )
            """
        )
        # sets an exclusive level advisory lock
        connection.execute("SELECT pg_advisory_xact_lock(%s)", (STATE_LOCK_ID,))
        # runs the query to insert the store data
        connection.execute(
            f"""
            INSERT INTO {STATE_TABLE} (state_id, payload)
            VALUES (1, %s)
            ON CONFLICT (state_id) DO NOTHING
            """,
            (Jsonb(create_store()),),
        )
        # gets the data from the DB and sets it into row
        row = connection.execute(
            f"SELECT payload FROM {STATE_TABLE} WHERE state_id = 1 FOR UPDATE"
        ).fetchone()
        # checks that the data was returned, error handling
        if row is None:
            raise RuntimeError("The evaluation state row could not be initialized")
        return connection, row["payload"]

    # if it is unable to make a connection with the database it rolls back and 
    # closes the connection before raising an error
    except Exception:
        connection.rollback()
        connection.close()
        raise
```


```
# Runs a query to update the data in the DB is needed otherwise it rolls back
# and closes the connection to the database.
# It is good that it checks if changes were made or not in order to make sure the 
# DB remains up to date
def finish_database_request(
    connection: Connection, store: dict[str, Any], persist: bool
) -> None:
    try:
        if persist:
            # update the DB if changes were made
            connection.execute(
                f"UPDATE {STATE_TABLE} SET payload = %s WHERE state_id = 1",
                (Jsonb(store),),
            )
            connection.commit()
        else:
            # roll back any changes otherwise
            connection.rollback()
    finally:
        # close the connection to the DB
        connection.close()
```

```
# When an http request is made, it connects the API handlers to the database
# when things are working correctly it will load the JSONB and locks the database
# so it is available to the handler before the JSONB is commited to the DB if the connection was made.
# otherwise there was some error 
@app.middleware("http")
async def postgres_state_middleware(request: Request, call_next: Any) -> Response:
    # Tests can supply an isolated store without requiring a running PostgreSQL server.

    # if a test is being run it will enter through here and use the store
    if hasattr(request.app.state, "store"):
        request.state.store = request.app.state.store
        return await call_next(request)

    # gets the database url from the environment
    database_url = os.getenv("DATABASE_URL")
    # if the URL could not be found it returns an error message that the DB was 
    # not configured and returns a 503 status code error
    if not database_url:
        logger.error("DATABASE_URL is not configured")
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"detail": "Database is not configured"},
        )

    connection = None
    # when making multiple calls, they don't block FastAPIs async event loop
    try:
        # they wait until they are able to be run 
        connection, store = await run_in_threadpool(load_database_state, database_url)
        request.state.store = store
        response = await call_next(request)
        request_connection, connection = connection, None
        await run_in_threadpool(
            finish_database_request,
            request_connection,
            request.state.store,
            response.status_code < status.HTTP_400_BAD_REQUEST,
        )
        return response
    # if there is some DB error from psycopg raise an error immediately because
    # the DB failed in some form
    except PsycopgError:
        if connection is not None:
            request_connection, connection = connection, None
            await run_in_threadpool(
                finish_database_request, request_connection, {}, False
            )
        logger.exception("PostgreSQL request failed")
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"detail": "Database request failed"},
        )
    # if there is an exception then there is some other error and raise an error
    except Exception:
        if connection is not None:
            request_connection, connection = connection, None
            await run_in_threadpool(
                finish_database_request, request_connection, {}, False
            )
        raise
```

```
# Gets the store that contains mock data. It doe have error handling that it 
# does exist, but does not have checks to make sure all components like 
# a rubric having criterions do exist
def store_for(request: Request) -> dict[str, Any]:
    if hasattr(request.state, "store"):
        return request.state.store
    raise RuntimeError("Request store was not initialized")

```

```
# get different items from the store (reviews, criterions, etc.)
# There is error handling in the case that the items do not exist
# otherwise it returns the items
def get_item(items: dict[str, Any], key: str, kind: str) -> dict[str, Any]:
    item = items.get(key)
    if item is None:
        raise HTTPException(status_code=404, detail=f"{kind} not found")
    return item
```

```
# Gets the projects from their scopeItype (project, course, lab)
# It is a bit unusual that projects is handled completely different compared to
# courses or labs when lines 456-460 would work for 'project' as well
def projects_for_scope(
    store: dict[str, Any], scope_type: str, scope_id: str
) -> list[dict[str, Any]]:
    # if the scope type is projects get it from its scope_id
    if scope_type == "project":
        project = store["projects"].get(scope_id)
        # if it not empty send the project(s) otherwise sent an empty list
        return [project] if project is not None else []

    # otherwise, will get the course or lab projects
    return [
        project
        for project in store["projects"].values()
        if project[f"{scope_type}_id"] == scope_id
    ]

```

```
# Ensures that a rubric is in use by a project (connected to a project)
def rubric_is_in_use(store: dict[str, Any], rubric_id: str) -> bool:
    # returns first instance of it being true otherwise returns false 
    return any(
        project["rubric_id"] == rubric_id for project in store["projects"].values()
    )

```

```
# checks the scores of the reviews, get_item already checks that the project must exist
# before returning it. It further checks that the rubric ID has to exist before attempting 
# to use get_item to get the rubric and its criterion. The error handling for these are good, however, 
# it does not do error handling for the criterion. While it should be saved in Rubrics,
# if something went wrong, it does not check that it exists and may crash the service.
# That being said, there is error handling for making sure there are not duplicate 
# criterion IDs that were scored (accidentally scoring a criterion twice) and 
# the case where the number of scores for submission and criterions are not equal 
# (missing scores for a criterion or too many scores submitted given the number of criterions).
# There is also error handling for the scores to not exceed the max points avilable for 
# a criterion

def check_review_scores(
    store: dict[str, Any], project_id: str, scores: list[ScoreInput]
) -> None:
    # checks the project exists and retrieves it
    project = get_item(store["projects"], project_id, "Project")

    # get rurbic ID from the project information
    rubric_id = project["rubric_id"]

    # error handling if the rubric ID for some reason did not exist
    # which would be a total failure in storing data
    if rubric_id is None:
        raise HTTPException(status_code=409, detail="Project has no governing rubric")

    # gets the rubric if it exists
    rubric = get_item(store["rubrics"], rubric_id, "Rubric")

    # gets criterion from the rubric, but does not verify that they exist. No validation
    criteria = {item["criterion_id"]: item for item in rubric["criteria"]}

    # get the different criterion IDs for scoring purposes
    # if criterion did not get saved for some reason, this would not run, an error 
    # would be raised
    submitted_ids = [score.criterion_id for score in scores]

    # error handling for if someone scored a criterion twice
    if len(set(submitted_ids)) != len(submitted_ids):
        raise HTTPException(status_code=422, detail="Duplicate criterion score")
    
    # error handling if there is a discrepancy between number of submitted scores
    # and number of criterions needed.
    if set(submitted_ids) != set(criteria):
        raise HTTPException(
            status_code=422,
            detail="Scores must match all criteria in the project rubric",
        )

    # loop through scores to make sure that the score is not greater than 
    # the max points set for the given criteria 
    for score in scores:
        criterion = criteria[score.criterion_id]
        if score.score > criterion["max_points"]:
            raise HTTPException(
                status_code=422,
                detail=f"Score exceeds max_points for {score.criterion_id}",
            )

```

```
# Calculates the grade of the project from the rubric
# but does not do any error handling to ensure the project, rubric, 
# or criterions exist
def review_grade(store: dict[str, Any], review: dict[str, Any]) -> float:
    # get the project
    project = store["projects"][review["project_id"]]

    # get the rubric
    rubric = store["rubrics"][project["rubric_id"]]

    # get the criteria
    criteria = {item["criterion_id"]: item for item in rubric["criteria"]}

    # calculates total score across all criterions taking into account the weight of 
    # each criterion. returns percent of grade
    return sum(
        (score["score"] / criteria[score["criterion_id"]]["max_points"])
        * criteria[score["criterion_id"]]["weight"]
        * 100
        for score in review["scores"]
    )

```

```
# Statistical analysis of the project from all its scores from a student_peer or faculty_instructor
# It does lack some error handling to ensure a summary cannot be made if there 
# are no reviews. it also does not check that the project, criterion, or rubric exist
def role_summary(
    store: dict[str, Any], project_id: str, role: ReviewRole
) -> dict[str, Any]:
    # gets all the reviews from the same project
    # no error handling if there are zero reviews available
    reviews = [
        review
        for review in store["reviews"].values()
        if review["project_id"] == project_id and review["reviewer_role"] == role
    ]

    # Get the rubric, error handing is in get_item
    rubric = get_item(
        store["rubrics"],
        store["projects"][project_id]["rubric_id"],
        "Rubric",
    )

    # creates a list of each reviewed persons scores
    # There is no error handling for the rubric's existence
    grades = [review_grade(store, review) for review in reviews]
    mean_scores = {}

    # for each criterion in the rubric 
    # There is no error handling to ensure there are existing criterions
    for criterion in rubric["criteria"]:
        # loop through the scores for each review to get the score of ea criterion
        values = [
            score["score"]
            for review in reviews
            for score in review["scores"]
            if score["criterion_id"] == criterion["criterion_id"]
        ]

        # calculate the mean for the criterion
        mean_scores[criterion["criterion_id"]] = {
            "mean": fmean(values) if values else None,
            "weighted_grade_mean": (
                fmean(values) / criterion["max_points"] * criterion["weight"] * 100
                if values
                else None
            ),
            "evaluation_count": len(values),
        }

    # where does the grade belong in a grade scale
    distribution = {
        band: sum(1 for grade in grades if low <= grade < high)
        for band, low, high in [
            ("A", 90, 101),
            ("B", 80, 90),
            ("C", 70, 80),
            ("D", 60, 70),
            ("F", 0, 60),
        ]
    }

    # return the statistics generated
    return {
        "statistics": {
            "review_count": len(reviews),
            "average_score": fmean(grades) if grades else None,
            "standard_deviation": pstdev(grades) if len(grades) > 1 else 0.0,
            "weighted_grade_trend": [
                {
                    "submitted_at": review["submitted_at"],
                    "weighted_grade": review_grade(store, review),
                }
                for review in sorted(reviews, key=lambda item: item["submitted_at"])
            ],
        },
        "mean_scores": {
            "overall_weighted_grade": fmean(grades) if grades else None,
            "criteria": mean_scores,
        },
        "grade_distribution": distribution,
    }

```

```
# check health of the API
@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
```

```
# Creates a rubric
# does error handling for if the rubric is already being used by another project
# and if the project type is not course, project, or lab
# There is no authorization that only valid users can request this call
# There is no validation that the current user has permission to request to create a rubric
@app.post(
    f"{API_PREFIX}/rubrics",
    status_code=status.HTTP_201_CREATED,
)
def create_rubric(body: RubricCreate, request: Request) -> dict[str, Any]:
    store = store_for(request)
    # get the project

    # get a project from a project, course, lab from its scope_type and scope_id
    projects = projects_for_scope(store, body.scope_type, body.scope_id)
    scope_exists = (
        # get scope_id
        body.scope_id in store["projects"]
        # if it is a "project"
        if body.scope_type == "project"
        # otherwise it is a lab or course
        else body.scope_id in store[f"{body.scope_type}s"]
    )

    # error handling if it did not exist as a project, course, or lab
    if not scope_exists:
        raise HTTPException(status_code=404, detail="Rubric scope not found")

    # checks if the rubric is already connected to some other project
    if any(project["rubric_id"] is not None for project in projects):
        raise HTTPException(
            status_code=409, detail="A scoped project already has a governing rubric"
        )

    # Create timestamp for rubric
    timestamp = now_utc()
    # ceate new ID for the rubric
    rubric_id = new_id()

    # rubric data that will be inserted 
    rubric = {
        "rubric_id": rubric_id,
        "name": body.name,
        "description": body.description,
        "scope_type": body.scope_type,
        "scope_id": body.scope_id,
        "created_at": timestamp,
        "updated_at": timestamp,
        "criteria": [
            {"criterion_id": new_id(), **criterion.model_dump()}
            for criterion in body.criteria
        ],
    }

    # store the new rubric data
    store["rubrics"][rubric_id] = rubric
    # make sure it exists
    for project in projects:
        project["rubric_id"] = rubric_id
    return rubric

```

```
# There is no authorization check that only valid users can request this call
# There is no validation that the current user has permission to request all listing rubrics
# or specific variations that would send all projects, all courses, or all labs. Not just 
# ones that the user has access to 
@app.get(f"{API_PREFIX}/rubrics")
def list_rubrics(
    request: Request,
    project_id: str | None = None,
    course_id: str | None = None,
    lab_id: str | None = None,
) -> list[dict[str, Any]]:
    store = store_for(request)
    # filters for rubrics
    filters = [
        ("project", project_id),
        ("course", course_id),
        ("lab", lab_id),
    ]

    # loops through the filters to figure out what filters are desired, otherwise sets 
    # it to none aka no filters were submitted
    active_filter = next(((kind, value) for kind, value in filters if value), None)

    # error handling for if no filters were sent
    if active_filter is None:
        # sends all rubrics back
        # there is no validation that the correct faculty_instructor is attempting 
        # to access rubrics their rubrics 
        return list(store["rubrics"].values())
    kind, scope_id = active_filter

    # filtering for projects
    if kind == "project":
        # gets the project information
        project = store["projects"].get(scope_id or "")

        # error handling that the project scope exists
        if project is None:
            raise HTTPException(status_code=404, detail="Project not found")

        # gets ids of projects
        rubric_ids = {project["rubric_id"]} if project["rubric_id"] else set()
    # otherwise it was a course or lab
    else:
        # did not find courses or labs in scope_types
        if scope_id not in store[f"{kind}s"]:
            raise HTTPException(status_code=404, detail=f"{kind.title()} not found")
        
        # loop through rubrics items for specific courses or labs
        scoped_rubrics = {
            rubric_id
            for rubric_id, rubric in store["rubrics"].items()
            if rubric["scope_type"] == kind and rubric["scope_id"] == scope_id
        }

        # loop through the courses or labs 
        project_rubrics = {
            project["rubric_id"]
            for project in projects_for_scope(store, kind, scope_id or "")
            if project["rubric_id"] is not None
        }
        rubric_ids = scoped_rubrics | project_rubrics

    # return items that fit the criteria 
    return [
        store["rubrics"][rubric_id] for rubric_id in rubric_ids if rubric_id is not None
    ]

```

```
# Get a specific rubric
# Error validation is done through the get_item
# There is no authorization that a valid user is attempting to request this
# there is no validation that the user has the permissions to request this
@app.get(f"{API_PREFIX}/rubrics/{{rubric_id}}")
def get_rubric(rubric_id: str, request: Request) -> dict[str, Any]:
    return get_item(store_for(request)["rubrics"], rubric_id, "Rubric")

```

```
# Updating a rubric given its rubric_id
# There is no authorization that a valid user is attempting to request this
# there is no validation that the user has the permissions to request this
@app.put(f"{API_PREFIX}/rubrics/{{rubric_id}}")
def update_rubric(
    rubric_id: str, body: RubricUpdate, request: Request
) -> dict[str, Any]:
    store = store_for(request)
    # get the rubric
    rubric = get_item(store["rubrics"], rubric_id, "Rubric")

    # if the rubric is already being used in a project currently
    if rubric_is_in_use(store, rubric_id):
        raise HTTPException(status_code=409, detail="Rubric is in use")

    # otherwise update the rubric
    rubric.update(body.model_dump(exclude_unset=True, exclude_none=True))

    # and update the time 
    rubric["updated_at"] = now_utc()
    return rubric

```

```
# Deletes a rubric given its ID
# It is unexpected that the system would sent a no content http response instead 
# of some sucess status, otherwise it could give the wrong impression that the 
# item did not exist to be deleted in the first place.
# There is no authorization that a valid user is attempting to request this
# there is no validation that the user has the permissions to request this
@app.delete(
    f"{API_PREFIX}/rubrics/{{rubric_id}}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_rubric(rubric_id: str, request: Request) -> Response:
    store = store_for(request)

    # Error validation done here to retrieve the item to delete
    get_item(store["rubrics"], rubric_id, "Rubric")
    # if the rubric is being used it cannot be deleted
    if rubric_is_in_use(store, rubric_id):
        raise HTTPException(status_code=409, detail="Rubric is in use")

    # otherwise it can be deleted
    del store["rubrics"][rubric_id]
    return Response(status_code=status.HTTP_204_NO_CONTENT)

```

```
# Returns summary of an individual project including the scores that
# faculty_instructor and student_peer made
# There is no authorization that a valid user is attempting to request this
# there is no validation that the user has the permissions to request this
@app.get(f"{API_PREFIX}/projects/{{project_id}}/summary")
def project_summary(project_id: str, request: Request) -> dict[str, Any]:
    store = store_for(request)
    # get the project
    project = get_item(store["projects"], project_id, "Project")

    # Error handling for if the project does not have an existing rubric
    if project["rubric_id"] is None:
        raise HTTPException(status_code=409, detail="Project has no governing rubric")

    # otherwise, return the project ID, the summary of faculty_instructor scores and student_peer scores
    return {
        "project_id": project_id,
        "faculty_instructor": role_summary(store, project_id, "faculty_instructor"),
        "student_peer": role_summary(store, project_id, "student_peer"),
    }

```

```
# Submit a review for a specific project. Validates that there are no errors in 
# the current reviews before doing so.
# There is no authorization that a valid user is attempting to request this
# there is no validation that the user has the permissions to request this
@app.post(
    f"{API_PREFIX}/projects/{{project_id}}/reviews",
    status_code=status.HTTP_201_CREATED,
)
def submit_review(
    project_id: str, body: ReviewCreate, request: Request
) -> dict[str, Any]:
    store = store_for(request)
    # Get the project the review is for
    get_item(store["projects"], project_id, "Project")

    # check that the current scores are valid, so that a review cannot be 
    # submitted if there exist errors with the reviews already 
    check_review_scores(store, project_id, body.scores)
    review_id = new_id()
    # New review 
    review = {
        "review_id": review_id,
        "project_id": project_id,
        "reviewer_role": body.reviewer_role,
        "submitted_at": now_utc(),
        "scores": [score.model_dump() for score in body.scores],
    }

    # Save the review
    store["reviews"][review_id] = review
    return review

```

```
# list reviews for a project given specific parameters 
# There is no authorization that a valid user is attempting to request this
# there is no validation that the user has the permissions to request this
@app.get(f"{API_PREFIX}/projects/{{project_id}}/reviews")
def list_reviews(
    project_id: str,
    request: Request,
    min_grade: Annotated[float | None, Query(ge=0, le=100)] = None,
    sort_by: Literal["grade", "submitted_at"] = "submitted_at",
    sort_order: Literal["asc", "desc"] = "asc",
) -> list[dict[str, Any]]:
    store = store_for(request)
    # Get the project
    get_item(store["projects"], project_id, "Project")

    # for all reviews if the review project ID matches the project ID
    # and the score for reviews are above the minimum score
    reviews = [
        review
        for review in store["reviews"].values()
        if review["project_id"] == project_id
        and (min_grade is None or review_grade(store, review) >= min_grade)
    ]

    # return the reviews by the established sort order
    return sorted(
        reviews,
        key=lambda review: (
            review_grade(store, review)
            if sort_by == "grade"
            else review["submitted_at"]
        ),
        reverse=sort_order == "desc",
    )
```

```
# Get the review by its review ID and project ID
# There is no authorization that a valid user is attempting to request this
# there is no validation that the user has the permissions to request this
@app.get(f"{API_PREFIX}/projects/{{project_id}}/reviews/{{review_id}}")
def get_review(project_id: str, review_id: str, request: Request) -> dict[str, Any]:
    store = store_for(request)
    # Get the review by its review ID
    review = get_item(store["reviews"], review_id, "Review")

    # if the review's project ID does not match the project_id then an error is raised
    if review["project_id"] != project_id:
        raise HTTPException(status_code=404, detail="Review not found for project")
    return review
```
```
# Update a review by ID for a project, project ID is also used
# has error validation for if the project ID does not match the rubric's project ID
# There is no authorization that a valid user is attempting to request this
# there is no validation that the user has the permissions to request this
@app.put(f"{API_PREFIX}/projects/{{project_id}}/reviews/{{review_id}}")
def update_review(
    project_id: str,
    review_id: str,
    body: ReviewUpdate,
    request: Request,
) -> dict[str, Any]:
    store = store_for(request)
    # get the review
    review = get_item(store["reviews"], review_id, "Review")

    # if the review's project ID does not match the project ID given, raise an error
    if review["project_id"] != project_id:
        raise HTTPException(status_code=404, detail="Review not found for project")
    # stores updated review
    updates = body.model_dump(exclude_unset=True, exclude_none=True)

    # checks that the updated version has scores (may or may not have values)
    if "scores" in updates:
        # checks the scores are valid inputs
        check_review_scores(store, project_id, body.scores or [])
    # updates the review 
    review.update(updates)
    return review
```

```
# Deletes a review
# Returns a status code of 204 NO_CONTENT, which is a bit misleading as someone
# can assume there was no content found to delete so it ran into some error.
# There is no authorization that a valid user is attempting to request this
# there is no validation that the user has the permissions to request this
@app.delete(
    f"{API_PREFIX}/projects/{{project_id}}/reviews/{{review_id}}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_review(project_id: str, review_id: str, request: Request) -> Response:
    store = store_for(request)
    # get the review
    review = get_item(store["reviews"], review_id, "Review")

    # check if the review's project ID is the same as the project ID 
    if review["project_id"] != project_id:
        raise HTTPException(status_code=404, detail="Review not found for project")
    # delete the review
    del store["reviews"][review_id]
    return Response(status_code=status.HTTP_204_NO_CONTENT)

```

```
# Generates a report of all projects in a project, course, lab
# Does error handling for if no project was found
# There is no authorization that a valid user is attempting to request this
# there is no validation that the user has the permissions to request this
@app.get(f"{API_PREFIX}/reports")
def reports(
    request: Request,
    course_id: str | None = None,
    lab_id: str | None = None,
    project_id: str | None = None,
    min_score: Annotated[float | None, Query(ge=0, le=100)] = None,
    sort_by: Literal["project_id", "mean_score"] = "project_id",
    sort_order: Literal["asc", "desc"] = "asc",
) -> Response:
    store = store_for(request)
    # list of projects given a [project_id, course_id, lab_id] was given
    # and the project is associated w a review
    projects = [
        project
        for project in store["projects"].values()
        if (project_id is None or project["project_id"] == project_id)
        and (course_id is None or project["course_id"] == course_id)
        and (lab_id is None or project["lab_id"] == lab_id)
        and project["rubric_id"] is not None
    ]

    # if no projects were found raise an error
    if project_id is not None and not projects:
        raise HTTPException(status_code=404, detail="Project not found")
    project_reports = []

    # for each project generate a summary 
    for project in projects:
        summary = project_summary(project["project_id"], request)
        # for both student_peers and faculty_instructors, get their respective scores
        grades = [
            role["mean_scores"]["overall_weighted_grade"]
            for role in (summary["faculty_instructor"], summary["student_peer"])
            if role["mean_scores"]["overall_weighted_grade"] is not None
        ]
        # if the scores are valid
        if min_score is not None and (not grades or max(grades) < min_score):
            continue
        project_reports.append(summary)

    # filter details for the report being generated
    report = {
        "filters": {
            "course_id": course_id,
            "lab_id": lab_id,
            "project_id": project_id,
            "min_score": min_score,
            "sort_by": sort_by,
            "sort_order": sort_order,
        },
        "projects": project_reports,
    }

    # if sorting by mean score
    if sort_by == "mean_score":
        # calculate mean grade for faculty_instructors and student_peer
        def mean_grade(summary: dict[str, Any]) -> float:
            grades = [
                # for faculty_instructor and student_peer get the mean scores
                summary[role]["mean_scores"]["overall_weighted_grade"]
                for role in ("faculty_instructor", "student_peer")
                if summary[role]["mean_scores"]["overall_weighted_grade"] is not None
            ]
            # return a total mean score
            return fmean(grades) if grades else -1

        # order report by mean scores
        report["projects"].sort(key=mean_grade, reverse=sort_order == "desc")
    else:
        # otherwise sort by project ID
        report["projects"].sort(
            key=lambda summary: summary["project_id"], reverse=sort_order == "desc"
        )
    # return JSON report in file
    return JSONResponse(
        content=report,
        headers={
            "Content-Disposition": 'attachment; filename="evaluation-report.json"'
        },
    )
```

#### SonarQube project properties
```# key for my project
sonar.projectKey=ramired2_CS763-proj
# the organization for my project
sonar.organization=ramired2
# main source for app 
sonar.sources=functional-codebase/app
# source for tests
sonar.tests=functional-codebase/tests
# type encoding being used 
sonar.sourceEncoding=UTF-8
# python version being used
sonar.python.version=3.12
```

#### Test.py (imports not included)
```
# helps with automized testing
client = TestClient(app)
```
```
# reset the store before ea test
@pytest.fixture(autouse=True)
def reset_store() -> None:
    app.state.store = deepcopy(create_store())
```

```
# retrieves a submitted project evaluation
def test_retrieving_a_submitted_evaluation() -> None:
    # gets the review for a project project-101
    response = client.get(f"{API_PREFIX}/projects/project-101/reviews")

    # check got code 200
    assert response.status_code == 200
    # get review in object
    reviews = response.json()

    # check review has reviews 101 and 102
    assert {review["review_id"] for review in reviews} == {"review-101", "review-102"}
    # check scores are in the review
    assert all(review["scores"] for review in reviews)
```

```
# submit an individual evaluation
def test_submitting_an_individual_evaluation() -> None:
    # gets response from creating a review 
    response = client.post(
        f"{API_PREFIX}/projects/project-101/reviews",
        json={
            "reviewer_role": "student_peer",
            "scores": [
                {
                    "criterion_id": "criterion-analysis",
                    "score": 4,
                    "feedback": "Reasoning is clear.",
                },
                {
                    "criterion_id": "criterion-design",
                    "score": 5,
                    "feedback": "The design is complete.",
                },
            ],
        },
    )

    # check got status code 201
    assert response.status_code == 201

    # get review in object format
    review = response.json()

    # check the reviewed project was "project-101"
    assert review["project_id"] == "project-101"
    # check the role was a student_peer
    assert review["reviewer_role"] == "student_peer"
    # check it contains feedback
    assert review["scores"][0]["feedback"] == "Reasoning is clear."
    # check the review ID not in the review
    assert "reviewer_id" not in review
```

```
# edit a rubric that is not in use
def test_editing_a_rubric_that_is_not_in_use() -> None:
    # get response of editing a rubric
    response = client.put(
        f"{API_PREFIX}/rubrics/rubric-102",
        json={"name": "Updated rubric", "description": "Updated description."},
    )

    # check status code was 200
    assert response.status_code == 200

    # check the response has name has the updated rubric name
    assert response.json()["name"] == "Updated rubric"
    # check the review has the updated description
    assert response.json()["description"] == "Updated description."
```

```
# delete a rubric that is not in use
def test_deleting_a_rubric_that_is_not_in_use() -> None:
    # get response for deleting a rubric
    response = client.delete(f"{API_PREFIX}/rubrics/rubric-102")

    # check the status code was 204
    assert response.status_code == 204
    # check the rubric ID is no longer in rubrics
    assert "rubric-102" not in app.state.store["rubrics"]
```

```
# create a new evaluation schema
def test_creating_an_evaluation_schema() -> None:
    # get response for creating an evaluation schema
    response = client.post(
        f"{API_PREFIX}/rubrics",
        json={
            "name": "CS503 rubric",
            "description": "Rubric for the CS503 course.",
            "scope_type": "course",
            "scope_id": "CS503",
            "criteria": [
                {
                    "name": "Research",
                    "description": "Research quality.",
                    "weight": 0.7,
                    "max_points": 5,
                },
                {
                    "name": "Communication",
                    "description": "Communication quality.",
                    "weight": 0.3,
                    "max_points": 5,
                },
            ],
        },
    )
    # check status code was 201
    assert response.status_code == 201
    # get rubric in object format
    rubric = response.json()
    # check it contains a course type
    assert rubric["scope_type"] == "course"
    # check the scope type is CS503
    assert rubric["scope_id"] == "CS503"
    # check the number of criterions is two
    assert len(rubric["criteria"]) == 2
```

```
# retrieve an aggregated summary report for a project
def test_retrieving_an_aggregated_summary_report_for_a_project() -> None:
    # get response for creating an individual project summary
    response = client.get(f"{API_PREFIX}/projects/project-101/summary")

    # check status code was 200
    assert response.status_code == 200

    # get summary in object format
    summary = response.json()

    # check summary has project ID project-101
    assert summary["project_id"] == "project-101"

    # for faculty_instructor and student_peer
    for role in ("faculty_instructor", "student_peer"):
        # check it has a statistics, mean_scores, and grade_distribution
        assert set(summary[role]) == {
            "statistics",
            "mean_scores",
            "grade_distribution",
        }

        # check it has at one review count
        assert summary[role]["statistics"]["review_count"] == 1

        # check the mean scores is above 0
        assert summary[role]["mean_scores"]["overall_weighted_grade"] > 0

        # check the sum of the grade distribution is one 
        assert sum(summary[role]["grade_distribution"].values()) == 1
```

```
# retrieve a specific review for a project
def test_retrieving_a_specific_review_for_a_project() -> None:
    # get a response for getting a specific review for a project
    response = client.get(f"{API_PREFIX}/projects/project-101/reviews/review-101")

    # check status code is 200
    assert response.status_code == 200

    # get review in object
    review = response.json()

    # check review ID was review-101
    assert review["review_id"] == "review-101"
    # check review was made by a faculty_instructor
    assert review["reviewer_role"] == "faculty_instructor"
```

```
# edit a specific review for a project
def test_editing_a_specific_review_for_a_project() -> None:
    # get response for editing a review for a project
    response = client.put(
        f"{API_PREFIX}/projects/project-101/reviews/review-101",
        json={
            "scores": [
                {
                    "criterion_id": "criterion-analysis",
                    "score": 3,
                    "feedback": "Updated analysis feedback.",
                },
                {
                    "criterion_id": "criterion-design",
                    "score": 4,
                    "feedback": "Updated design feedback.",
                },
            ]
        },
    )

    # check status code was 200
    assert response.status_code == 200
    # get review in object format
    review = response.json()

    # check score was updated to 3
    assert review["scores"][0]["score"] == 3
    # check feedback was updated to "updated analysis feedback"
    assert review["scores"][0]["feedback"] == "Updated analysis feedback."
```

```
# remove a specific review for a project
def test_removing_a_specific_review_for_a_project() -> None:
    # get response for deleting a review for a project
    response = client.delete(f"{API_PREFIX}/projects/project-101/reviews/review-101")

    # check response was 204
    assert response.status_code == 204
    # check review no longer exists in the store of reviews 
    assert "review-101" not in app.state.store["reviews"]
```

### 2.3 The AI Agent's "Security Sins" (Evaluating Code Deficiencies)
> The prompt I fed Copilot went into a bit of information of what I expected from it.
 While its main purpose was to create the functional-codebase folder with test 
 cases included as some subfolder, I specified the need for a happy path approach, 
 a definition of what 'functional-codebase' is meant to do and have based on the 
 master spec, and a series of test cases that need to be included. Copilot did attempt, 
 to use the spec.md from PA1, even after I mentioned in my prompt that the master spec be used,
  so I had to specify again where the code requirements and instructions should stem from. 
  Moreover, I did specify at some later point the need to include postgreSQL, where 
  Copilot mainly still uses the JSONB it initially created. 
  In terms of the code it generated, it does make sense why it would not focus 
  on using secure code as AI tends to need a specific instructions of how to do things. 
  Otherwise, it tends to jump to a lot of different conclusions which lead to unexpected results.  
  In this case, because I did not specify it should focus its efforts on making sure it 
  produces secure code for functional-codebase, it would not take security into account.
  Not unless it was mentioned in the master spec from where it pulled its information from.

> Without specifying security requirements in my prompts or modifying the master spec to include such 
information, the code falls into BOLA/IDOR, race conditions, and input injection vulnerabilities.
In terms of BOLA/IDOR, the code generated does expose a file name, and IDs of different projects, criterions, 
rubrics, etc. Not only that, but there is no authentication checks for a valid user or authorization for if a user has 
permission to perform speicifc API calls. As such, this could lead to valid student_peers attempting to create 
a report, which should only be allowed for a faculty_instructor. Or a student_peer attempting 
to access another student_peers review, which should remain anonymous. This was a major 
shortcut that Copilot took. As for race conditions, there is not a lot of concern, as when PostgreSQL
was added, Copilot put a lock in the definition load_database_state. There is concern for situations
 where the lock gets stuck and there is a queue of queries that don't get sent. 
There is also concerns for input injection, as none of the code sanitizes any inputs.
 It takes them at face value. This, would also be a big concern from the code 
 generated. 

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