CI/CD with Automated Testing

### Objective
Added unit tests for transformation logic and wire them into the DAB deployment pipeline so bad code can't reach production silently.

### Benefit
- Catches regressions before deploy — e.g., if someone changes the dedup key and it silently breaks
- Standard expectation in any mature data engineering role; "I have zero tests" is a common gap interviewers probe for
- Pairs naturally with your DAB setup from Step 7 — this is the missing piece that makes it real CI/CD, not just "CD"
