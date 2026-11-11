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
### Semgrep
There were zero false positives found.

### SonarQube
These were zero false positives found.


## 3 Distinct Vulnerabilities
| Vulnerability                                                                                                                                | Software Layer | Common Weakness Enumeration (CWE) ID | Technical Root-Cause Explanation                                                                                                                                                                                                        |
| -------------------------------------------------------------------------------------------------------------------------------------------- | :------------: | :----------------------------------: | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ./functional-codebase/main.py Lines 460-475 does not authenticate that a valid user is attempting to submit a review                         | Authentication |               CWE-306                | There is missing authentification for attempting to submit a review. A new user is created for every review. This action neglects checking if there are any existing users and whether the user has the permissions to submit a review. |
| ./functional-codebase/main.py Lines 530-540 does not check authorization that the owner or a review is attempting to delete their own review | Authorization  |               CWE-862                | Does not check for authorization if the current user is the owner of a review they are attempting to delete.                                                                                                                            |
| ./functional-codebase/main.py Line 503 does not check that the review ID is valid and is attached to a review                                |     Input      |                CWE-20                | Does not check that the ID exists and is valid before attemptingto get a review for a project                                                                                                                                                                                                                                        |