## Service Purpose
The Peer Review and Evaluation Gateway will use Python/FastAPI in order to create a service that will facilitate the process of assigning and evaluating student’s published works based on rubrics. The service will facilitate this process by creating and managing rubrics, assigning reviewers for published works, and tracking the scores of said published works. Reviewers could be faculty, course instructors, or students while all published works would belong to other students. 

### Technology Stack
* Python/ FastAPI

## API Endpoints
| Method | Path | Description |
| :----- | ---- | ----------- |
| GET    | /api/v1/rubric/getRubric{course_id} |             |

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

### Mock Data

