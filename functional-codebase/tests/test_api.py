# Tool: Luna-6 GPT
#
# Prompt summary:   Create a FastAPI app given the requirements outlined in
#                   projectPortalDomain which was edited to only have the 
#                   Domain 3 information with 9 test cases
#
# AI Contribution: 95%
#
# Human Modifications: Added quick comments describing the purpose of each def
#

from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from app.main import API_PREFIX, app, create_store

client = TestClient(app)

# reset the store before ea test
@pytest.fixture(autouse=True)
def reset_store() -> None:
    app.state.store = deepcopy(create_store())

# retrieve a submitted evaluation for a project
def test_retrieving_a_submitted_evaluation() -> None:
    response = client.get(f"{API_PREFIX}/projects/project-101/reviews")

    assert response.status_code == 200
    reviews = response.json()
    assert {review["review_id"] for review in reviews} == {"review-101", "review-102"}
    assert all(review["scores"] for review in reviews)

# submit an individual evaluation
def test_submitting_an_individual_evaluation() -> None:
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

    assert response.status_code == 201
    review = response.json()
    assert review["project_id"] == "project-101"
    assert review["reviewer_role"] == "student_peer"
    assert review["scores"][0]["feedback"] == "Reasoning is clear."
    assert "reviewer_id" not in review

# edit a rubric that is not in use
def test_editing_a_rubric_that_is_not_in_use() -> None:
    response = client.put(
        f"{API_PREFIX}/rubrics/rubric-102",
        json={"name": "Updated rubric", "description": "Updated description."},
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Updated rubric"
    assert response.json()["description"] == "Updated description."

# delete a rubric that is not in use
def test_deleting_a_rubric_that_is_not_in_use() -> None:
    response = client.delete(f"{API_PREFIX}/rubrics/rubric-102")

    assert response.status_code == 204
    assert "rubric-102" not in app.state.store["rubrics"]

# create a new evaluation schema
def test_creating_an_evaluation_schema() -> None:
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
    assert response.status_code == 201
    rubric = response.json()
    assert rubric["scope_type"] == "course"
    assert rubric["scope_id"] == "CS503"
    assert len(rubric["criteria"]) == 2

# retrieve an aggregated summary report for a project
def test_retrieving_an_aggregated_summary_report_for_a_project() -> None:
    response = client.get(f"{API_PREFIX}/projects/project-101/summary")

    assert response.status_code == 200
    summary = response.json()
    assert summary["project_id"] == "project-101"
    for role in ("faculty_instructor", "student_peer"):
        assert set(summary[role]) == {
            "statistics",
            "mean_scores",
            "grade_distribution",
        }
        assert summary[role]["statistics"]["review_count"] == 1
        assert summary[role]["mean_scores"]["overall_weighted_grade"] > 0
        assert sum(summary[role]["grade_distribution"].values()) == 1

# retrieve a specific review for a project
def test_retrieving_a_specific_review_for_a_project() -> None:
    response = client.get(
        f"{API_PREFIX}/projects/project-101/reviews/review-101"
    )

    assert response.status_code == 200
    review = response.json()
    assert review["review_id"] == "review-101"
    assert review["reviewer_role"] == "faculty_instructor"

# edit a specific review for a project
def test_editing_a_specific_review_for_a_project() -> None:
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

    assert response.status_code == 200
    review = response.json()
    assert review["scores"][0]["score"] == 3
    assert review["scores"][0]["feedback"] == "Updated analysis feedback."

# remove a specific review for a project
def test_removing_a_specific_review_for_a_project() -> None:
    response = client.delete(
        f"{API_PREFIX}/projects/project-101/reviews/review-101"
    )

    assert response.status_code == 204
    assert "review-101" not in app.state.store["reviews"]
