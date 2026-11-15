## AI Usage Log
| AI Contribution % | Summary of prompt                                               |
| :---------------: | --------------------------------------------------------------- |
|        15%        | Sanity checking my initial entities                             |
|        5%         | explanation of what endpoints are usually used for JSON schemas |
|        20%        | Checking soundness of my initial JSON schemas                   |
|       100%        | Creation of mock data from my JSON schemas                      |

## Service Purpose
The Peer Review and Evaluation Gateway will use Python/FastAPI in order to create a service that will facilitate the process of assigning and evaluating published works based on rubrics. The service will facilitate this process by creating and managing rubrics, assigning reviewers for published works, and tracking the scores of said reviews of published works into an aggregate score. Reviewers could be faculty members, course instructors, or students while all published works would belong to other students. 

### Technology Stack
* Python/ FastAPI

## API Endpoints
### Rubric
| Path                               | Methods       | Description                                            |
| ---------------------------------- | :------------ | ------------------------------------------------------ |
| /api/v1/evals/rubrics/{course_id}     | GET<br>POST   | Initialize a rubric or get a rubric from the course ID |
| /api/v1/evals/rubrics/{assignment_id} | GET           | Get the rubric for an assignment                       |
| /api/v1/evals/rubrics/{rubric_id}     | PUT<br>DELETE | Edit or remove a rubric                                |

### rubric_criteria
| Path                                      | Methods       | Description                                                     |
| ----------------------------------------- | :------------ | --------------------------------------------------------------- |
| /api/v1/evals/rubricCriterias/{rubric_id}    | GET<br>POST   | Get criteria for a rubric<br>Initialize a criteria for a rubric |
| /api/v1/evals/rubricCriterias/{criteria_id} | PUT<br>DELETE | Edits a criterial field<br>Delete a criteria                    |

### Published_Work
| Path                                      | Methods       | Description                                                      |
| ----------------------------------------- | :------------ | ---------------------------------------------------------------- |
| /api/v1/evals/publishedWorks/{work_id}       | GET<br>DELETE | Gets a single published work<br>Deletes a published work         |
| /api/v1/evals/publishedWorks/{author_id}     | GET<br>POST   | Get works of a single author<br>    A user can submit their work |
| /api/v1/evals/publishedWorks/{assignment_id} | GET           | Gets works from a single assignment                              |

### Course
| Path                              | Methods | Description                                  |
| --------------------------------- | :------ | -------------------------------------------- |
| /api/v1/evals/courses/{course_id} | GET     | Get all assignmnets from a particular course |

### Review_session
| Path                                                   | Methods       | Description                                                |
| ------------------------------------------------------ | :------------ | ---------------------------------------------------------- |
| /api/v1/evals/reviewSessions/getSession/{assignment_id} | GET<br>POST   | Get a review session's details<br>Create a review session  |
| /api/v1/evals/reviewSessions/editSession/{session_id}   | PUT<br>DELETE | Edits a review session details<br>Deletes a review session |

### Assignment

| Path                                      | Methods              | Description                                                                                         |
| ----------------------------------------- | :------------------- | --------------------------------------------------------------------------------------------------- |
| /api/v1/evals/assignments/{assignment_id} | GET<br>PUT<br>DELETE | Get a single assignment<br>Change the rubric associated with the assignment<br>Delete an assignment |
| /api/v1/evals/assignments/{rubic_id}      | POST                 | Create an assignment                                                                                |

### Evaluation
| Path                                         | Methods     | Description                                                                                                              |
| -------------------------------------------- | :---------- | ------------------------------------------------------------------------------------------------------------------------ |
| /api/v1/evals/evaluations/{evaluation_id}    | GET<br>PUT  | Get an evaluation<br>Allows a reviewer to edit their evaluation                                                          |
| /api/v1/evals/evaluations/{user_id}          | GET         | Gets all evaluations assigned to a person                                                                                |
| /api/v1/evals/evaluations/{published_work_id}| POST<br>PUT | Creates an association with a reviewer and the published work they will review<br>Edit the reviewer for a published work |

### Reviewer_type
| Path | Methods                     | Description                                                 |
| ---- | :-------------------------- | ----------------------------------------------------------- |
| GET  | /api/v1/evals/reviewerTypes | Get reviewing options (faculty member, instructor, student) |

### Evaluation_score
| Path                                                     | Methods       | Description                                                                      |
| -------------------------------------------------------- | :------------ | -------------------------------------------------------------------------------- |
| /api/v1/evals/evaluationScores/{work_id}                 | GET           | Get all the scores from a published work                                         |
| /api/v1/evals/evaluationScores/{criteria_id}             | GET           | Get all scores per criteria                                                      |
| /api/v1/evals/evaluationScores/{reviewer_id}/{work_id}   | GET           | Get all scores from an assignment from a specific reviewer                       |
| /api/v1/evals/evaluationScores/{work_id}/{evaluation_id} | POST          | Allows a reviewer to evaluate a criteria                                         |
| /api/v1/evals/evaluationScores/{evaluation_score_id}     | PUT<br>DELETE | Allows a user to edit an evaluation score they set<br>Deletes a evaluation score |

### Aggregate_Score
| Path                                               | Methods       | Description                                                                                                                    |
| -------------------------------------------------- | :------------ | ------------------------------------------------------------------------------------------------------------------------------ |
| /api/v1/evals/aggregateScores/{criteria_id}        | GET           | Calculates all recorded scores for a single criteria                                                                           |
| /api/v1/evals/aggregateScores/{work_id}            | GET<br>POST   | Calculates all recorded scores for each criteria<br>Calculates and creates an entry of an assignments scores for each criteria |
| /api/v1/evals/aggregateScores/{aggregate_score_id} | PUT<br>DELETE | Updates the scores for all criteria for an assignment when a new evaluation score is updated.<br>Deletes an aggregated. score  |

### User
| Path                        | Methods | Description     |
| --------------------------- | :------ | --------------- |
| /api/v1/evals/users/{email} | GET     | Get a user's ID |

### Person
| Path                                              | Methods | Description                                            |
| ------------------------------------------------- | :------ | ------------------------------------------------------ |
| /api/v1/evals/persons/{user_id}/{course_id}       | POST    | Set the reviewer type for a user per course            |
| /api/v1/evals/persons/{reviewer_type}/{course_id} | GET     | Get all [students, faculty, instructors] from a course |

## Entity Relationships
|      Entity      | Attributes                                                                       | Relationships/ Constrains                                                                                                                                                                                                                                                            |
| :--------------: | -------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
|      Rubric      | rubric_id, name, description, date_created, date_modified, course_id             | One course has multiple Rubrics<br>Primary key: rubric_id<br>Foreign key: Rubric.course_id (Course.course_id)                                                                                                                                                                        |
| Rubric_Criteria  | criteria_id, rubric_id, criteria, description, min_score, max_score, weight      | One Rubric has multiple Rubric_criteria<br>Primary key: criteria_id<br> Foregin Key: Rubric_Criteria.rubric_id (Rubric.rubric_id)                                                                                                                                                    |
|  Published_work  | work_id, author_id, assignment_id, file, submission_date                         | Multiple Evaluation have one Published_works<br>Primary key: work_id<br> Foregin Key: Published_work.author_id (Person.id)<br> Foregin Key: Published_work.assignment_id (Assignment.id)                                                                                             |
|      Course      | course_id, name, instructor_id, start_date, end_date                             | One Person has multiple Courses<br>Primary key: course_id<br> Foregin Key: Course.instructor_id (Person.id)                                                                                                                                                                          |
|  Review_session  | session_id, assignment_id, start_date, end_date                                  | One Assignment has one Review_session<br>Primary key: session_id<br> Foregin Key: Review_session.assignment_id UNIQUE (Assignment.id)                                                                                                                                                |
|    Assignment    | id, name, rubric_id, description                                                 | One Rubric has multiple Assignments<br>Primary key: id<br> Foregin Key: Assignment.rubric_id (Rubric.rubric_id)                                                                                                                                                                      |
|    Evaluation    | evaluation_id, reviewer_id, work_id                                              | One Person has multiple Evaluations <br>One Published_work has multiple Evaluations<br>Primary key: evaluation_id<br> Foregin Key: Evaluation.reviewer_id (Person.id)<br> Foregin Key: Evaluation.work_id NOT UNIQUE (Published_work.work_id)                                        |
|  Reviewer_type   | reviewer_type_id, type (e.g. instructor, faculty member, student)                | One Person has many Reviewer_types<br>Primary_key: reviewer_type_id Reviewer_types                                                                                                                                                                                                   |
| Evaluation_score | evaluation_score_id, criteria_id, score, evaluation_id, feedback, submitted_date | One Rubric_criteria has many Evaluation_scores<br>Many Evaluations have many Evaluation_scores<br>primary key: evaluation_score_id<br>Foreign key: Evaluation_score.criteria (Rubric_criteria.criteria_id)<br>Foreign key: Evaluation_score.evaluation_id (Evaluation.evaluation_id) |
| Aggregate_score  | aggregate_score_id, work_id, criteria_id, score, evaluation_count                | One Aggregate_score has one Published work<br>One Aggregate_score has one Rubric_criteria<br> Foregin Key: Aggregate_score.criteria_id (rubric_criteria.criteria_id)<br> Foregin Key: Aggregate_score.work_id (Published_work.work_id)                                               |
|       User       | id, name, email, username                                                        | One user has multiple Persons<br>Primary key: id                                                                                                                                                                                                                                     |
|      Person      | id, user_id, reviewer_type_id, course_id                                         | One Reviewer_type has multiple Person<br>Primary key: id<br>Foreign key: Person.reviewer_type_id (Reviewer_type.reviewer_type_id)<br>Foreign key: Person.user_id (User.id)<br>Foreign key: Person.course_id (Course_id)                                                              |

## JSON Schemas
### Rubric
#### Creating a Rubric ```POST /api/v1/evals/rubrics/{course_id}```
```json
{
    "name": "Lab 1",
    "description":"rubric for Lab 1 that fufilled this weeks learning goals.",
    "rubric_criteria": [
        {
            "criteria":"Analysis",
            "description":"Student demonstrates thorough understanding of topic",
            "weight": 0.5,
            "min_score": 0,
            "max_score":5
        },
        {
            "criteria":"Completion",
            "description":"Student answered all questiones to the best of their abilities and submitted work on time",
            "weight":0.5,
            "min_score":0,
            "max_score":5
        }    
    ],
}
```

#### Editing a Rubric ```PUT /api/v1/evals/rubrics/{rubric_id}```
```json
{
    "name": "Lab 1",
    "description":"rubric for Lab 1 that fufilled this weeks learning goals.",
    "rubric_criteria": [
        {
            "criteria":"Analysis",
            "description":"Student demonstrates thorough understanding of topic",
            "weight": 0.5,
            "min_score": 0,
            "max_score":5
        },
        {
            "criteria":"Completion",
            "description":"Student answered all questiones to the best of their abilities and submitted work on time",
            "weight":0.5,
            "min_score":0,
            "max_score":5
        }    
    ]
}
```
### rubric_criteria
#### Add a New Criteria ```POST /api/v1/evals/rubricCriterias/{rubric_id} ```
```json
{
    "criteria":"Completion",
    "description":"Student answered all questiones to the best of their abilities and submitted work on time",
    "weight":0.5,
    "min_score":0,
    "max_score":5
}
```

#### Edit a Criteria ```PUT /api/v1/evals/rubricCriterias/{criteria_id}```
```json
{
    "criteria":"Completion",
    "description":"Student answered all questiones to the best of their abilities and submitted work on time",
    "weight":0.5,
    "min_score":0,
    "max_score":5
}
```
Weight sums for criteria must equal to 1. 

### Published_Work
#### Publish a Work   ```POST /api/v1/evals/publishedWorks/{author_id}```
```json
{
    "assignment_id": "assign-134",
    "file":"multipart/form-data"
}
```

### Review_session
#### Create/Edit a Reviewing Session ```POST/PUT /api/v1/evals/reviewSessions/{assignment_id}```
```json
{
    "start_date": "2025-10-31T00:00:00Z",
    "end_date":"2025-11-10T00:00:00Z"
}
```
start_date < end_date

### Assignment
#### Create an Assignment ```POST /api/v1/evals/assignments/{rubic_id} ```
```json
{
    "name": "Lab 1",
    "description":"Instructions follow..."
}
```

#### Edit an Assignment ```PUT /api/v1/evals/assignments/{assignment_id}```
```json
{
    "name": "Lab 2",
    "description":"Instructions follow this..."
}
```

### Evaluation
#### Create an Evaluation/ Edit Reviewer for Published Work ```POST /api/v1/evals/evaluations/{published_work_id}```
```json
{
    "reviewer_id": "person-1573"
}
```

#### Edit en Evaluation ```PUT /api/v1/evals/evaluations/{evaluation_id}```
```json
{
    "reviewer_id": "person-389",
    "submission_date":null
}
```

### Evaluation Score
#### Create an Evaluation Score ```POST /api/v1/evals/evaluationScores/{work_id}/{evaluation_id} ```
```json
{
    "criteria_id": "criteria-134",
    "score": 4,
    "feedback":"good job showcasing analysis of lab questions"
}
```
#### Edit an Evaluation ```PUT /api/v1/evals/evaluationScores/{evaluation_score_id}```
```json
{
    "score": 4,
    "feedback":"good job showcasing analysis of lab questions"
}
```

### Aggregate_Score
#### Create an Agrgegated Score for a Criteria ```POST /api/evals/aggregateScores/{work_id}```
```json
{
    "criteria_id": "temp",
    "score":4.6,
    "evaluation_count": 3
}
```
#### Update an Agrgegated Score for a Criteria ```POST /api/evals/aggregateScores/{aggregate_score_id}```
```json
{
    "criteria_id": "temp",
    "score":4.6,
    "evaluation_count": 3
}
```

### Person
#### Set a Person's Reviewer Type (Student, Facilitator, Instructor) ```POST /api/evals/persons/{user_id}/{course_id} ```
```json
{
    "reviewer_type_id": "instructor-12"
}
```

### Mock Data

* IDs are fake
* timestamps use UTC
* Each evaluation score references a criterion in the rubric used by the work's assignment
* Aggregate scores are averages of submitted evaluation scores for that work and criterion
  * (sum of all scores submitted for a criterion from a single work) / (count of evaluations)

```json
{
  "courses": [
    {
      "course_id": "course-101",
      "name": "Introduction to Computing",
      "instructor_id": "person-101",
      "start_date": "2026-09-01",
      "end_date": "2026-12-18"
    }
  ],
  "reviewer_types": [
    {
      "reviewer_type_id": "role-student",
      "type": "student"
    },
    {
      "reviewer_type_id": "role-instructor",
      "type": "instructor"
    }
  ],
  "users": [
    {
      "id": "user-101",
      "name": "Alex Chen",
      "email": "alex@example.test",
      "username": "alexchen"
    },
    {
      "id": "user-102",
      "name": "Jordan Lee",
      "email": "jordan@example.test",
      "username": "jordanlee"
    },
    {
      "id": "user-103",
      "name": "Sam Rivera",
      "email": "sam@example.test",
      "username": "samrivera"
    },
    {
      "id": "user-104",
      "name": "Taylor Morgan",
      "email": "taylor@example.test",
      "username": "taylormorgan"
    }
  ],
  "persons": [
    {
      "id": "person-101",
      "user_id": "user-101",
      "reviewer_type_id": "role-instructor",
      "course_id": "course-101"
    },
    {
      "id": "person-102",
      "user_id": "user-102",
      "reviewer_type_id": "role-student",
      "course_id": "course-101"
    },
    {
      "id": "person-103",
      "user_id": "user-103",
      "reviewer_type_id": "role-student",
      "course_id": "course-101"
    },
    {
      "id": "person-104",
      "user_id": "user-104",
      "reviewer_type_id": "role-student",
      "course_id": "course-101"
    }
  ],
  "rubrics": [
    {
      "rubric_id": "rubric-101",
      "name": "Lab 1 Rubric",
      "description": "Evaluate the analysis and completeness of Lab 1.",
      "date_created": "2026-09-05T16:00:00Z",
      "date_modified": "2026-09-05T16:00:00Z",
      "course_id": "course-101"
    }
  ],
  "rubric_criteria": [
    {
      "criteria_id": "criterion-101",
      "rubric_id": "rubric-101",
      "criteria": "Analysis",
      "description": "Explains the approach and reasoning.",
      "min_score": 0,
      "max_score": 5,
      "weight": 0.6
    },
    {
      "criteria_id": "criterion-102",
      "rubric_id": "rubric-101",
      "criteria": "Completion",
      "description": "Addresses all required parts of the assignment.",
      "min_score": 0,
      "max_score": 5,
      "weight": 0.4
    }
  ],
  "assignments": [
    {
      "id": "assignment-101",
      "name": "Lab 1",
      "rubric_id": "rubric-101",
      "description": "Submit a short analysis of the assigned problem."
    }
  ],
  "review_sessions": [
    {
      "session_id": "session-101",
      "assignment_id": "assignment-101",
      "start_date": "2026-10-01T00:00:00Z",
      "end_date": "2026-10-15T23:59:59Z"
    }
  ],
  "published_works": [
    {
      "work_id": "work-101",
      "author_id": "person-102",
      "assignment_id": "assignment-101",
      "file": "works/work-101.pdf",
      "submission_date": "2026-10-02T18:30:00Z"
    }
  ],
  "evaluations": [
    {
      "evaluation_id": "evaluation-101",
      "reviewer_id": "person-103",
      "work_id": "work-101"
    },
    {
      "evaluation_id": "evaluation-102",
      "reviewer_id": "person-104",
      "work_id": "work-101"
    }
  ],
  "evaluation_scores": [
    {
      "evaluation_score_id": "score-101",
      "criteria_id": "criterion-101",
      "score": 4,
      "evaluation_id": "evaluation-101",
      "feedback": "The reasoning is clear and well supported.",
      "submitted_date": "2026-10-08T17:00:00Z"
    },
    {
      "evaluation_score_id": "score-102",
      "criteria_id": "criterion-102",
      "score": 5,
      "evaluation_id": "evaluation-101",
      "feedback": "All required parts are included.",
      "submitted_date": "2026-10-08T17:00:00Z"
    },
    {
      "evaluation_score_id": "score-103",
      "criteria_id": "criterion-101",
      "score": 5,
      "evaluation_id": "evaluation-102",
      "feedback": "Strong analysis with a sound explanation.",
      "submitted_date": "2026-10-09T14:30:00Z"
    },
    {
      "evaluation_score_id": "score-104",
      "criteria_id": "criterion-102",
      "score": 4,
      "evaluation_id": "evaluation-102",
      "feedback": "One minor requirement could be clearer.",
      "submitted_date": "2026-10-09T14:30:00Z"
    }
  ],
  "aggregate_scores": [
    {
      "aggregate_score_id": "aggregate-101",
      "work_id": "work-101",
      "criteria_id": "criterion-101",
      "score": 4.5,
      "evaluation_count": 2
    },
    {
      "aggregate_score_id": "aggregate-102",
      "work_id": "work-101",
      "criteria_id": "criterion-102",
      "score": 4.5,
      "evaluation_count": 2
    }
  ]
}
```
