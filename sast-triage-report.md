# SAST Triage Report

## AI Usage Log
| AI Contribution % | Summary of prompt   |
| :---------------: | ------------------- |
|        0%         | No AI has been used |

## True Positives
Semgrep reported 0 findings even after using the rulesets: p/python, p/owasp-top-ten, and p/security-audit.
SonarQube reported 0 vulnerabilities or security hotspots.

### Semgrep
There were zero true positives found.

### SonarQube
There were zero true positives found.

## False Positives
Semgrep reported 0 findings even after using the rulesets: p/python, p/owasp-top-ten, and p/security-audit.
SonarQube reported 0 vulnerabilities or security hotspots.
### Semgrep
There were zero false positives found.

### SonarQube
These were zero false positives found.


## 3 Distinct Vulnerabilities
| Vulnerability                                                                                                                         | Software Layer | Common Weakness Enumeration (CWE) ID | Technical Root-Cause Explanation                                                                                                                                                                                           |
| ------------------------------------------------------------------------------------------------------------------------------------- | :------------: | :----------------------------------: | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ./functional-codebase/main.py Lines 460-475 does not authenticate that a the individual attempting to submit a review is a valid user | Authentication |               CWE-306                | Definition does not check authentification of individual attempting to submit a review. A new user is created for every review, therefore the current individual could not be a valid user.                                |
| ./functional-codebase/main.py Lines 530-540 Does not check that the current user has authorization to delete a review                 | Authorization  |               CWE-862                | Definition does not check authorization of the individual attempting to delete a review. It does not check that the current individual is a valid user who wrote the review and has permission to delete their own review. |
| ./functional-codebase/main.py Line 503 does not check that the review ID is valid and is attached to a review                         |     Input      |                CWE-20                | Definition does not validate that the review ID exists. It assumes it exists and attempts to retreive a project.                                                                                                           |