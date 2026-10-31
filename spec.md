## Service Purpose
The Peer Review and Evaluation Gateway will use Python/FastAPI in order to create a service that will facilitate the process of assigning and evaluating student’s published works based on rubrics. The service will facilitate this process by creating and managing rubrics, assigning reviewers for published works, and tracking the scores of said published works. Reviewers could be faculty, course instructors, or students while all published works would belong to other students. 

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
| Method | Path                                        | Description                          |
| :----- | ------------------------------------------- | ------------------------------------ |
| GET    | /api/v1/publishedWork/changeScore/{work_id} | Change the score of a published work |

### Course
| Method | Path                                            | Description                                  |
| :----- | ----------------------------------------------- | -------------------------------------------- |
| GET    | /api/v1/course/assignmentsPerCourse/{course_id} | Get all assignmnets from a particular course |

### Review_session
| Method | Path                                                            | Description                    |
| :----- | --------------------------------------------------------------- | ------------------------------ |
| POST   | /api/v1/reviewSession/createSession/{rubric_id}/{assignment_id} | Create a review session        |
| PUT    | /api/v1/reviewSession/editSession/{session_id}                  | Edits a review session details |
| DELETE | /api/v1/reviewSession/deleteSession/{session_id}                | Deletes a review session |

### Assignment
| Method | Path                                                | Description                                      |
| :----- | --------------------------------------------------- | ------------------------------------------------ |
| PUT    | /api/v1/assignment/{assignment_id}                  | Change the rubric associated with the assignment |
| GET    | /api/v1/assignment/getCourseAssignments/{course_id} | Get all assignmnets from a course |

### Evaluation
| Method | Path                                                   | Description                                                    |
| :----- | ------------------------------------------------------ | -------------------------------------------------------------- |
| POST   | /api/v1/Evaluation/assignEvaluator/{published_work_id} | Sets a reviewer for a published work                           |
| PUT    | /api/v1/Evaluation/editEvaluator/{published_work_id}   | Edit the reviewer for a published work                         |
| DELETE | /api/v1/Evaluation/deleteEvaluation/{evaluation_id}    | Revokes a reviewer from evaluating a published work            |
| POST   | /api/v1/Evaluation/makeEvaluation/{evaluation_id}      | Allows a reviewer to create an evaluation for a published work |
| PUT    | /api/v1/Evaluation/editEvaluatin/{evaluation_id}       | Allows a reviewer to edit their evaluation                     |

### Reviewer_type
| Method | Path                                   | Description                                              |
| :----- | -------------------------------------- | -------------------------------------------------------- |
| GET    | /api/v1/Reviewer_type/getReviewerTypes | Get reviewing options (facilitator, instructor, student) |

### Person
| Method | Path                             | Description    |
| :----- | -------------------------------- | -------------- |
| GET    | /api/v1/Person/getUserId/{email} | Get a users id |




## Entity Relationships
|     Entity      | Attributes                                                                     | Relationships/ Constrains                                                                                                                                                                                                         |
| :-------------: | ------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|     Rubric      | rubric_id, name, description, date_created, date_modified, course_id           | One course has multiple Rubrics<br>Primary key: rubric_id<br>Foreign key: Rubric.course_id (Course.course_id)                                                                                                                     |
| Rubric_Criteria | criteria_id, rubric_id, criteria, description, min_score, max_score            | One Rubric has multiple Rubric_criteria<br>Primary key: criteria_id<br> Foregin Key: Rubric_Criteria.rubric_id (Rubric.rubric_id)                                                                                                 |
| Published_work  | work_id, author_id, assignment_id, file, submission_date, final_score          | One Evaluation has one Published_work<br>Primary key: work_id<br> Foregin Key: Published_work.author_id (Person.id)<br> Foregin Key: Published_work.assignment_id (Assignment.id)                                                 |
|     Course      | course_id, name, instructor_id, start_date, end_date                           | One Person has multiple Courses<br>Primary key: course_id<br> Foregin Key: Courses.instructor_id (Person.id)                                                                                                                      |
| Review_session  | session_id, rubric_id, assignment_id, start_date, end_date                     | One Rubric has one Review_session<br>Primary key: session_id<br> Foregin Key: Review_session.rubric_id (Rubric.rubric_id)<br> Foregin Key: Published_work.assignment_id (Assignment.id)                                           |
|   Assignment    | id, course_id, rubric_id, description                                          | One Rubric has multiple Assignments<br>One Course has multiple Assignments<br>Primary key: id<br> Foregin Key: Assignment.rubric_id (Rubric.rubric_id)<br> Foregin Key: Assignment.course_id (Course.course_id)                   |
|   Evaluation    | evaluation_id, reviewer_id, published_work_id, feedback, score, submitted_date | One Person has multiple Evaluations <br>One Published_work has one Evaluation<br>Primary key: evaluation_id<br> Foregin Key: Evaluation.reviewer_id (Person.id)<br> Foregin Key: Evaluation.published_work_id (Published_work.id) |
|  Reviewer_type  | reviewer_type_id, type (e.g. instructor, faculty member, student)              | Primary_key: reviewer_type_id Reviewer_types                                                                                                                                                                                      |
|     Person      | id, name, reviewer_type_id, email, username, password                          | One Reviewer_type has multiple Persons<br>Primary key: id<br>Foreign key: Person.reviewer_type_id (Reviewer_type.reviewer_type_id)                                                                                                |

## JSON Schemas

```json
{
    "quick_ex": "rand",
    "quick_example": "random"
}
```

### Mock Data

