## Service Purpose
The Peer Review and Evaluation Gateway will use Python/FastAPI in order to create a service that will facilitate the process of assigning and evaluating published works based on rubrics. The service will facilitate this process by creating and managing rubrics, assigning reviewers for published works, and tracking the scores of said reviews of published works into an aggregate score. Reviewers could be faculty members, course instructors, or students while all published works would belong to other students. 

### Technology Stack
* Python/ FastAPI

## API Endpoints
### Rubric
| Method | Path                                     | Description                      |
| :----- | ---------------------------------------- | -------------------------------- |
| GET    | /api/v1/rubric/getAllRubrics/{course_id} | Get all rubrics from a course    |
| GET    | /api/v1/rubric/getRubric/{assignment_id} | Get the rubric for an assignment |
| POST   | /api/v1/rubric/createRubric/{course_id}  | Create a rubric                  |
| PUT    | /api/v1/rubric/editRurbic/{rubric_id}    | Edit a rurbic                    |
| DELETE | /api/v1/rubric/deleteRubric/{rubric_id}  | Delete a rubric                  |

### Rurbic_criteria
| Method | Path                                                | Description                       |
| :----- | --------------------------------------------------- | --------------------------------- |
| GET    | /api/v1/rubricCriteria/getCriteria/{rubric_id}      | Get criteria for a rubric         |
| POST   | /api/v1/rubricCriteria/addCriteria/{rurbic_id}      | Adds a new criteria to rubric     |
| PUT    | /api/v1/rubricCriteria/editCriteria/{criteria_id}   | Edits a criterial field           |
| DELETE | /api/v1/rurbicCriteria/deleteCriteria/{criteria_id} | Delete a criterie from the rubric |

### Published_Work
| Method | Path                                                         | Description                         |
| :----- | ------------------------------------------------------------ | ----------------------------------- |
| GET    | /api/v1/publishedWork/getWork/{work_id}                      | Gets a single published work        |
| GET    | /api/v1/publishedWork/getsWorksAuthor/{author_id}            | Get works of a single author        |
| GET    | /api/v1/publishedWork/getWorksFromAssignment/{assignment_id} | Gets works from a single assignment |
| POST   | /api/v1/publishedWork/submitWork/{author_id}                 | A user can submit their work        |
| DELETE | /api/v1/publishedWork/deleteWork/{work_id}                   | Deletes a published work            |

### Course
| Method | Path                                            | Description                                  |
| :----- | ----------------------------------------------- | -------------------------------------------- |
| GET    | /api/v1/course/assignmentsPerCourse/{course_id} | Get all assignmnets from a particular course |

### Review_session
| Method | Path                                                | Description                    |
| :----- | --------------------------------------------------- | ------------------------------ |
| GET    | /api/v1/reviewSession/getSession/{assignment_id}    | Get a review session's details |
| POST   | /api/v1/reviewSession/createSession/{assignment_id} | Create a review session        |
| PUT    | /api/v1/reviewSession/editSession/{session_id}      | Edits a review session details |
| DELETE | /api/v1/reviewSession/deleteSession/{session_id}    | Deletes a review session       |

### Assignment
| Method | Path                                             | Description                                      |
| :----- | ------------------------------------------------ | ------------------------------------------------ |
| GET    | /api/v1/assignment/getAssignment/{assignment_id} | Get a single assignment                          |
| PUT    | /api/v1/assignment/changeRubric/{assignment_id}  | Change the rubric associated with the assignment |
| POST   | /api/v1/assignment/createAssignment/{rubic_id}  | Create an assignment                             |
| DELETE | /api/v1/assignment/{assignment_id}               | Delete an assignment                             |

### Evaluation
| Method | Path                                                   | Description                                                                    |
| :----- | ------------------------------------------------------ | ------------------------------------------------------------------------------ |
| GET    | /api/v1/Evaluations/getEvaluation/{evaluation_id}      | Get an evaluation                                                              |
| GET    | /api/v1/Evaluations/getAssignedEvaluations/{user_id}   | Gets all evaluations assigned to a person                                      |
| POST   | /api/v1/Evaluation/assignEvaluator/{published_work_id} | Creates an association with a reviewer and the published work they will review |
| PUT    | /api/v1/Evaluation/editEvaluator/{published_work_id}   | Edit the reviewer for a published work                                         |
| PUT    | /api/v1/Evaluation/setSubmisionDate/{evaluation_id}    | Edits the submission date for the evaluation                                   |
| PUT    | /api/v1/Evaluation/editEvaluatin/{evaluation_id}       | Allows a reviewer to edit their evaluation                                     |

### Reviewer_type
| Method | Path                                    | Description                                                 |
| :----- | --------------------------------------- | ----------------------------------------------------------- |
| GET    | /api/v1/Reviewer_type/getReviewerTypes/ | Get reviewing options (faculty member, instructor, student) |

### Evaluation_score
| Method | Path                                                                   | Description                                                |
| :----- | ---------------------------------------------------------------------- | ---------------------------------------------------------- |
| GET    | /api/v1/Evaluation_score/getAllScoresFromWork/{work_id}                | Get all the scores from a published work                   |
| GET    | /api/v1/Evaluation_score/getScoresCriteria/{criteria_id}               | Get all scores per criteria                                |
| GET    | /api/v1/Evaluation_score/getScoresFromReviewer/{reviewer_id}/{work_id} | Get all scores from an assignment from a specific reviewer |
| POST   | /api/v1/Evaluation_score/scoreCriteria/{work_id/evaluation_id}         | Allows a reviewer to evaluate a criteria                   |
| PUT    | /api/v1/Evaluation_score/editEvaluation/{evaluation_score_id}                | Allows a user to edit an evaluation score they set          |
| DELETE | /api/v1/Evaluation_score/deleteEvaluationScore/{evaluation_score_id}   | Deletes a evaluation score                                 |


### Aggregate_Score
| Method | Path                                                           | Description                                                                |
| :----- | -------------------------------------------------------------- | -------------------------------------------------------------------------- |
| GET    | /api/v1/Aggregate_Score/calculateScore/{criteria_id}           | Calculates all recorded scores for a single criteria                       |
| GET    | /api/v1/Aggregate_Score/calculateAllCriteria/{work_id}         | Calculates all recorded scores for each criteria                           |
| POST   | /api/v1/Aggregate_Score/createGrade{work_id}                   | Calculates and creates an entry of an assignments scores for each criteria |
| PUT    | /api/v1/Aggregate_Score/updateScore/{aggregate_score_id}          | Updates the scores for all criteria for an assignment when a new evaluation score is updated.                     |
| DELETE | /api/v1/Aggregate_Score/deleteAggregateScore/{aggregate_score_id} | Deletes an aggregated. score                                                |

### User
| Method | Path                           | Description    |
| :----- | ------------------------------ | -------------- |
| GET    | /api/v1/user/getUserId/{email} | Get a users id |
|        |                                |                |

### Person
| Method | Path                                                   | Description                                            |
| :----- | ------------------------------------------------------ | ------------------------------------------------------ |
| POST   | /api/v1/Person/setUserType/{user_id}/{course_id}       | Set the reviewer type for a user per course            |
| GET    | /api/v1/Person/setUserType/{reviewer_type}/{course_id} | Get all [students, faculty, instructors] from a course |




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
| Aggregate_score  | aggregate_score_id, work_id, criteria_id, score, evaluation_count                | One Aggregate_score has one Published work<br>One Aggregate_score has one Rubric_criteria<br> Foregin Key: Aggregate_score.criteria_id (Rurbic_criteria.criteria_id)<br> Foregin Key: Aggregate_score.work_id (Published_work.work_id)                                               |
|       User       | id, name, email, username, password                                              | One user has multiple Persons<br>Primary key: id                                                                                                                                                                                                                                     |
|      Person      | id, user_id, reviewer_type_id, course_id                                         | One Reviewer_type has multiple Person<br>Primary key: id<br>Foreign key: Person.reviewer_type_id (Reviewer_type.reviewer_type_id)<br>Foreign key: Person.user_id (User.id)<br>Foreign key: Person.course_id (Course_id)                                                              |

## JSON Schemas
### Rubric
#### Creating a Rubric ```POST /api/v1/rubric/createRubric/{course_id}```
```json
{
    "name": "Lab 1",
    "description":"Rurbic for Lab 1 that fufilled this weeks learning goals.",
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

#### Editing a Rubric ```PUT /api/v1/rubric/createRubric/{rubric_id}```
```json
{
    "name": "Lab 1",
    "description":"Rurbic for Lab 1 that fufilled this weeks learning goals.",
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
### Rurbic_criteria
#### Add a New Criteria ```POST /api/v1/rubricCriteria/addCriteria/{rurbic_id} ```
```json
{
    "criteria":"Completion",
    "description":"Student answered all questiones to the best of their abilities and submitted work on time",
    "weight":0.5,
    "min_score":0,
    "max_score":5
}
```

#### Edit a Criteria ```PUT /api/v1/rubricCriteria/editCriteria/{criteria_id}```
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
#### Publish a Work   ```POST /api/v1/publishedWork/submitWork/{author_id}```
```json
{
    "assignment_id": "assign-134",
    "file":"multipart/form-data"
}
```

### Review_session
#### Create/Edit a Reviewing Session ```POST /api/v1/reviewSession/createSession/{assignment_id}```/ ```PUT /api/v1/reviewSession/editSession/{session_id}```
```json
{
    "start_date": "2025-10-31T00:00:00Z",
    "end_date":"2025-11-10T00:00:00Z"
}
```
start_date < end_date

### Assignment
#### Create an Assignment ```POST /api/v1/assignment/createAssignment/{rubic_id} ```
```json
{
    "name": "Lab 1",
    "description":"Instructions follow..."
}
```

#### Edit an Assignment ```PUT /api/v1/assignment/changeRubric/{assignment_id}```
```json
{
    "name": "Lab 2",
    "description":"Instructions follow this..."
}
```

### Evaluation
#### Create an Evaluation ```POST /api/v1/Evaluation/assignEvaluator/{published_work_id} ```
```json
{
    "reviewer_id": "person-1573"
}
```

#### Edit en Evaluation ```PUT /api/v1/Evaluation/editEvaluatin/{evaluation_id}```
```json
{
    "reviewer_id": "person-389",
    "submission_date":null
}
```

#### Edits the Date of an Evaluation Submission Date ```PUT /api/v1/Evaluation/setSubmisionDate/{evaluation_id}```
```json
{
    "submission_date": "2025-11-10T00:00:00Z"
}
```


### Evaluation Score
#### Create an Evaluation Score ```POST /api/v1/Evaluation_score/scoreCriteria/{work_id}/{evaluation_id} ```
```json
{
    "criteria_id": "criteria-134",
    "score": 4,
    "feedback":"good job showcasing analysis of lab questions"
}
```
#### Edit an Evaluation ```PUT /api/v1/Evaluation_score/editEvaluation/{evaluation_score_id}```
```json
{
    "score": 4,
    "feedback":"good job showcasing analysis of lab questions"
}
```

### Aggregate_Score
#### Create an Agrgegated Score for a Criteria ```POST /api/v1/Aggregate_Score/createGrade{work_id}```
```json
{
    "criteria_id": "temp",
    "score":4.6,
    "evaluation_count": 3
}
```
#### Update an Agrgegated Score for a Criteria ```POST /api/v1/Aggregate_Score/createGrade{aggregate_score_id}```
```json
{
    "criteria_id": "temp",
    "score":4.6,
    "evaluation_count": 3
}
```

### Person
#### Set a Person's Reviewer Type (Student, Facilitator, Instructor) ```POST /api/v1/Person/setUserType/{user_id}/{course_id} ```
```json
{
    "reviewer_type_id": "instructor-12"
}
```

### Mock Data

