# # Tool: Luna-6 GPT
#
# Prompt summary:   Create a FastAPI app given the requirements outlined in
#                   projectPortalDomain which was edited to only have the 
#                   Domain 3 information with 9 test cases
#
# AI Contribution: 95%
#
# Human Modifications:  Added quick comments describing the purpose of each 
#                       function and class, remove unused json import, and
#                       use datetime.UTC for now_utc()
#

from __future__ import annotations

from datetime import datetime, UTC
from math import isclose
from statistics import fmean, pstdev
from typing import Annotated, Any, Literal
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Query, Request, Response, status
from pydantic import BaseModel, Field, model_validator
from starlette.responses import JSONResponse

API_PREFIX = "/api/v1/evaluations"
ReviewRole = Literal["faculty_instructor", "student_peer"]
ScopeType = Literal["project", "course", "lab"]

# create new ID
def new_id() -> str:
    return str(uuid4())

# return UTC timestamp
def now_utc() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds").replace(
        "+00:00", "Z"
    )

# single criteria in a rubric
class Criterion(BaseModel):
    name: str
    description: str
    weight: float = Field(gt=0, le=1)
    max_points: float = Field(gt=0)

# create rubric w criteria and scope
class RubricCreate(BaseModel):
    name: str
    description: str = ""
    scope_type: ScopeType
    scope_id: str
    criteria: list[Criterion] = Field(min_length=1)

    # makes sure criteria weights sum to 1
    @model_validator(mode="after")
    def weights_total_one(self) -> RubricCreate:
        if not isclose(sum(item.weight for item in self.criteria), 1.0):
            raise ValueError("Criterion weights must sum to 1")
        return self

# update rubric w criteria
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

# input score in a review
class ScoreInput(BaseModel):
    criterion_id: str
    score: float = Field(ge=0)
    feedback: str

# create a review w a reviewer role and scores
class ReviewCreate(BaseModel):
    reviewer_role: ReviewRole
    scores: list[ScoreInput] = Field(min_length=1)

# update a review w a reviewer role and scores
class ReviewUpdate(BaseModel):
    reviewer_role: ReviewRole | None = None
    scores: list[ScoreInput] | None = Field(default=None, min_length=1)

# create a store to hold courses, labs, projects, rubrics, and reviews
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
        "courses": {"CS501", "CS502", "CS503"},
        "labs": {"lab-cybersec", "lab-systems", "lab-unused"},
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


app = FastAPI(title="Peer Review and Evaluation Gateway", version="1.0.0")
app.state.store = create_store()

# get store from request
def store_for(request: Request) -> dict[str, Any]:
    return request.app.state.store

# get item from store 
# err 404 if not found
def get_item(items: dict[str, Any], key: str, kind: str) -> dict[str, Any]:
    item = items.get(key)
    if item is None:
        raise HTTPException(status_code=404, detail=f"{kind} not found")
    return item

# get projects from scope, type, and id
def projects_for_scope(
    store: dict[str, Any], scope_type: str, scope_id: str
) -> list[dict[str, Any]]:
    if scope_type == "project":
        project = store["projects"].get(scope_id)
        return [project] if project is not None else []
    return [
        project
        for project in store["projects"].values()
        if project[f"{scope_type}_id"] == scope_id
    ]

# check if rurbic is being used by any project
def rubric_is_in_use(store: dict[str, Any], rubric_id: str) -> bool:
    return any(
        project["rubric_id"] == rubric_id for project in store["projects"].values()
    )

# check review scores for duplicates, missing criteria, and exceeding max points
def check_review_scores(
    store: dict[str, Any], project_id: str, scores: list[ScoreInput]
) -> None:
    project = get_item(store["projects"], project_id, "Project")
    rubric_id = project["rubric_id"]
    if rubric_id is None:
        raise HTTPException(status_code=409, detail="Project has no governing rubric")
    rubric = get_item(store["rubrics"], rubric_id, "Rubric")
    criteria = {item["criterion_id"]: item for item in rubric["criteria"]}
    submitted_ids = [score.criterion_id for score in scores]
    if len(set(submitted_ids)) != len(submitted_ids):
        raise HTTPException(status_code=422, detail="Duplicate criterion score")
    if set(submitted_ids) != set(criteria):
        raise HTTPException(
            status_code=422, detail="Scores must match all criteria in the project rubric"
        )
    for score in scores:
        criterion = criteria[score.criterion_id]
        if score.score > criterion["max_points"]:
            raise HTTPException(
                status_code=422,
                detail=f"Score exceeds max_points for {score.criterion_id}",
            )

# calc weighted grade for review using rubric criteria weights and max points
def review_grade(store: dict[str, Any], review: dict[str, Any]) -> float:
    project = store["projects"][review["project_id"]]
    rubric = store["rubrics"][project["rubric_id"]]
    criteria = {item["criterion_id"]: item for item in rubric["criteria"]}
    return sum(
        (score["score"] / criteria[score["criterion_id"]]["max_points"])
        * criteria[score["criterion_id"]]["weight"]
        * 100
        for score in review["scores"]
    )

# calc summary/statistics of reviews for a project and role
#  includes mean scores, grade distribution
def role_summary(
    store: dict[str, Any], project_id: str, role: ReviewRole
) -> dict[str, Any]:
    reviews = [
        review
        for review in store["reviews"].values()
        if review["project_id"] == project_id and review["reviewer_role"] == role
    ]
    rubric = get_item(
        store["rubrics"],
        store["projects"][project_id]["rubric_id"],
        "Rubric",
    )
    grades = [review_grade(store, review) for review in reviews]
    mean_scores = {}
    for criterion in rubric["criteria"]:
        values = [
            score["score"]
            for review in reviews
            for score in review["scores"]
            if score["criterion_id"] == criterion["criterion_id"]
        ]
        mean_scores[criterion["criterion_id"]] = {
            "mean": fmean(values) if values else None,
            "weighted_grade_mean": (
                fmean(values) / criterion["max_points"] * criterion["weight"] * 100
                if values
                else None
            ),
            "evaluation_count": len(values),
        }
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

# check health of the API
@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}

# create a rubric
@app.post(
    f"{API_PREFIX}/rubrics",
    status_code=status.HTTP_201_CREATED,
)
def create_rubric(body: RubricCreate, request: Request) -> dict[str, Any]:
    store = store_for(request)
    projects = projects_for_scope(store, body.scope_type, body.scope_id)
    scope_exists = (
        body.scope_id in store["projects"]
        if body.scope_type == "project"
        else body.scope_id in store[f"{body.scope_type}s"]
    )
    if not scope_exists:
        raise HTTPException(status_code=404, detail="Rubric scope not found")
    if any(project["rubric_id"] is not None for project in projects):
        raise HTTPException(
            status_code=409, detail="A scoped project already has a governing rubric"
        )
    timestamp = now_utc()
    rubric_id = new_id()
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
    store["rubrics"][rubric_id] = rubric
    for project in projects:
        project["rubric_id"] = rubric_id
    return rubric

# list rubrics 
@app.get(f"{API_PREFIX}/rubrics")
def list_rubrics(
    request: Request,
    project_id: str | None = None,
    course_id: str | None = None,
    lab_id: str | None = None,
) -> list[dict[str, Any]]:
    store = store_for(request)
    filters = [
        ("project", project_id),
        ("course", course_id),
        ("lab", lab_id),
    ]
    active_filter = next(((kind, value) for kind, value in filters if value), None)
    if active_filter is None:
        return list(store["rubrics"].values())
    kind, scope_id = active_filter
    if kind == "project":
        project = store["projects"].get(scope_id or "")
        if project is None:
            raise HTTPException(status_code=404, detail="Project not found")
        rubric_ids = {project["rubric_id"]} if project["rubric_id"] else set()
    else:
        if scope_id not in store[f"{kind}s"]:
            raise HTTPException(status_code=404, detail=f"{kind.title()} not found")
        scoped_rubrics = {
            rubric_id
            for rubric_id, rubric in store["rubrics"].items()
            if rubric["scope_type"] == kind and rubric["scope_id"] == scope_id
        }
        project_rubrics = {
            project["rubric_id"]
            for project in projects_for_scope(store, kind, scope_id or "")
            if project["rubric_id"] is not None
        }
        rubric_ids = scoped_rubrics | project_rubrics
    return [
        store["rubrics"][rubric_id]
        for rubric_id in rubric_ids
        if rubric_id is not None
    ]

# get rubric by ID
@app.get(f"{API_PREFIX}/rubrics/{{rubric_id}}")
def get_rubric(rubric_id: str, request: Request) -> dict[str, Any]:
    return get_item(store_for(request)["rubrics"], rubric_id, "Rubric")

# update rubric by ID
@app.put(f"{API_PREFIX}/rubrics/{{rubric_id}}")
def update_rubric(
    rubric_id: str, body: RubricUpdate, request: Request
) -> dict[str, Any]:
    store = store_for(request)
    rubric = get_item(store["rubrics"], rubric_id, "Rubric")
    if rubric_is_in_use(store, rubric_id):
        raise HTTPException(status_code=409, detail="Rubric is in use")
    rubric.update(body.model_dump(exclude_unset=True, exclude_none=True))
    rubric["updated_at"] = now_utc()
    return rubric

# delete rubric by ID
@app.delete(
    f"{API_PREFIX}/rubrics/{{rubric_id}}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_rubric(rubric_id: str, request: Request) -> Response:
    store = store_for(request)
    get_item(store["rubrics"], rubric_id, "Rubric")
    if rubric_is_in_use(store, rubric_id):
        raise HTTPException(status_code=409, detail="Rubric is in use")
    del store["rubrics"][rubric_id]
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# get summary of reviews for one project
@app.get(f"{API_PREFIX}/projects/{{project_id}}/summary")
def project_summary(project_id: str, request: Request) -> dict[str, Any]:
    store = store_for(request)
    project = get_item(store["projects"], project_id, "Project")
    if project["rubric_id"] is None:
        raise HTTPException(status_code=409, detail="Project has no governing rubric")
    return {
        "project_id": project_id,
        "faculty_instructor": role_summary(store, project_id, "faculty_instructor"),
        "student_peer": role_summary(store, project_id, "student_peer"),
    }

# submit review for a project
@app.post(
    f"{API_PREFIX}/projects/{{project_id}}/reviews",
    status_code=status.HTTP_201_CREATED,
)
def submit_review(
    project_id: str, body: ReviewCreate, request: Request
) -> dict[str, Any]:
    store = store_for(request)
    get_item(store["projects"], project_id, "Project")
    check_review_scores(store, project_id, body.scores)
    review_id = new_id()
    review = {
        "review_id": review_id,
        "project_id": project_id,
        "reviewer_role": body.reviewer_role,
        "submitted_at": now_utc(),
        "scores": [score.model_dump() for score in body.scores],
    }
    store["reviews"][review_id] = review
    return review

# list reviews for project
@app.get(f"{API_PREFIX}/projects/{{project_id}}/reviews")
def list_reviews(
    project_id: str,
    request: Request,
    min_grade: Annotated[float | None, Query(ge=0, le=100)] = None,
    sort_by: Literal["grade", "submitted_at"] = "submitted_at",
    sort_order: Literal["asc", "desc"] = "asc",
) -> list[dict[str, Any]]:
    store = store_for(request)
    get_item(store["projects"], project_id, "Project")
    reviews = [
        review
        for review in store["reviews"].values()
        if review["project_id"] == project_id
        and (min_grade is None or review_grade(store, review) >= min_grade)
    ]
    return sorted(
        reviews,
        key=lambda review: (
            review_grade(store, review) if sort_by == "grade" else review["submitted_at"]
        ),
        reverse=sort_order == "desc",
    )

# get review by ID for project
@app.get(f"{API_PREFIX}/projects/{{project_id}}/reviews/{{review_id}}")
def get_review(project_id: str, review_id: str, request: Request) -> dict[str, Any]:
    store = store_for(request)
    review = get_item(store["reviews"], review_id, "Review")
    if review["project_id"] != project_id:
        raise HTTPException(status_code=404, detail="Review not found for project")
    return review

# update review by ID for project
@app.put(f"{API_PREFIX}/projects/{{project_id}}/reviews/{{review_id}}")
def update_review(
    project_id: str,
    review_id: str,
    body: ReviewUpdate,
    request: Request,
) -> dict[str, Any]:
    store = store_for(request)
    review = get_item(store["reviews"], review_id, "Review")
    if review["project_id"] != project_id:
        raise HTTPException(status_code=404, detail="Review not found for project")
    updates = body.model_dump(exclude_unset=True, exclude_none=True)
    if "scores" in updates:
        check_review_scores(store, project_id, body.scores or [])
    review.update(updates)
    return review

# delete review by ID for project
@app.delete(
    f"{API_PREFIX}/projects/{{project_id}}/reviews/{{review_id}}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_review(project_id: str, review_id: str, request: Request) -> Response:
    store = store_for(request)
    review = get_item(store["reviews"], review_id, "Review")
    if review["project_id"] != project_id:
        raise HTTPException(status_code=404, detail="Review not found for project")
    del store["reviews"][review_id]
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# generate report of projects w review summaries
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
    projects = [
        project
        for project in store["projects"].values()
        if (project_id is None or project["project_id"] == project_id)
        and (course_id is None or project["course_id"] == course_id)
        and (lab_id is None or project["lab_id"] == lab_id)
        and project["rubric_id"] is not None
    ]
    if project_id is not None and not projects:
        raise HTTPException(status_code=404, detail="Project not found")
    project_reports = []
    for project in projects:
        summary = project_summary(project["project_id"], request)
        grades = [
            role["mean_scores"]["overall_weighted_grade"]
            for role in (summary["faculty_instructor"], summary["student_peer"])
            if role["mean_scores"]["overall_weighted_grade"] is not None
        ]
        if min_score is not None and (
            not grades or max(grades) < min_score
        ):
            continue
        project_reports.append(summary)
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
    if sort_by == "mean_score":
        def mean_grade(summary: dict[str, Any]) -> float:
            grades = [
                summary[role]["mean_scores"]["overall_weighted_grade"]
                for role in ("faculty_instructor", "student_peer")
                if summary[role]["mean_scores"]["overall_weighted_grade"] is not None
            ]
            return fmean(grades) if grades else -1

        report["projects"].sort(key=mean_grade, reverse=sort_order == "desc")
    else:
        report["projects"].sort(
            key=lambda summary: summary["project_id"], reverse=sort_order == "desc"
        )
    return JSONResponse(
        content=report,
        headers={"Content-Disposition": 'attachment; filename="evaluation-report.json"'},
    )
