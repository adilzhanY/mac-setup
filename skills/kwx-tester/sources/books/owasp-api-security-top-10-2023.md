# OWASP API Security Top 10 (2023)

- Author: OWASP API Security Project
- Year: 2023
- Legal URL: https://api-security.owasp.org/editions/2023/en/0x11-t10 ; https://api-security.owasp.org/editions/2023/en/0xa1-broken-object-level-authorization

## What I read

The top 10 list and the API1 (BOLA) page with its prevention list.

## Key lessons used in backend/api-testing.md (also backend.md)

- API1 Broken Object Level Authorization, API2 Broken Authentication, API3 Broken Object Property Level Authorization, API4 Unrestricted Resource Consumption, API5 Broken Function Level Authorization, through API10.
- Prevention: "Write tests to evaluate the vulnerability of the authorization mechanism. Do not deploy changes that make the tests fail."
- Prefer random, unpredictable ids.
