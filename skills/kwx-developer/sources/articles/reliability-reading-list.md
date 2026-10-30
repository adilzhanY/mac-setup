# Reliability reading list (reliability/ folder)

Status: R = read in full, P = read in part (key sections), S = searched or summarized only.

## Google SRE (free books, sre.google)

- R https://sre.google/sre-book/monitoring-distributed-systems/
- R https://sre.google/sre-book/handling-overload/
- R https://sre.google/sre-book/addressing-cascading-failures/
- R https://sre.google/sre-book/release-engineering/
- R https://sre.google/sre-book/postmortem-culture/
- P https://sre.google/sre-book/practical-alerting/
- P https://sre.google/sre-book/embracing-risk/
- P https://sre.google/sre-book/service-level-objectives/
- P https://sre.google/sre-book/testing-reliability/
- P https://sre.google/workbook/alerting-on-slos/
- P https://sre.google/workbook/canarying-releases/
- P https://sre.google/workbook/monitoring/
- P https://sre.google/workbook/postmortem-culture/

## AWS Builders' Library

- R https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/
- R https://aws.amazon.com/builders-library/ensuring-rollback-safety-during-deployments/
- R https://aws.amazon.com/builders-library/implementing-health-checks/
- R https://aws.amazon.com/builders-library/avoiding-fallback-in-distributed-systems/
- P https://aws.amazon.com/builders-library/automating-safe-hands-off-deployments/
- P https://aws.amazon.com/builders-library/instrumenting-distributed-systems-for-operational-visibility/
- P https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/
- P https://aws.amazon.com/builders-library/avoiding-insurmountable-queue-backlogs/
- P https://aws.amazon.com/builders-library/using-load-shedding-to-avoid-overload/
- downloaded, not used: static-stability-using-availability-zones, going-faster-with-continuous-delivery

## Testing

- P https://abseil.io/resources/swe-book/html/ch11.html (Testing overview)
- P https://abseil.io/resources/swe-book/html/ch12.html (Unit testing)
- P https://abseil.io/resources/swe-book/html/ch13.html (Test doubles)
- P https://abseil.io/resources/swe-book/html/ch14.html (Larger testing)
- R https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html (post body, from raw HTML)
- S https://testing.googleblog.com/2010/12/test-sizes.html (body did not render; table values from memory of the post and the SWE book)
- S https://testing.googleblog.com/2013/08/testing-on-toilet-test-behavior-not.html (body did not render; comments only)
- S https://testing.googleblog.com/2015/01/testing-on-toilet-change-detector-tests.html (body did not render)
- P https://martinfowler.com/articles/practical-test-pyramid.html (Ham Vocke)
- P https://martinfowler.com/articles/nonDeterminism.html
- P https://kentcdodds.com/blog/the-testing-trophy-and-testing-classifications
- P https://kentcdodds.com/blog/write-tests
- P https://kentcdodds.com/blog/common-mistakes-with-react-testing-library
- P https://kentcdodds.com/blog/effective-snapshot-testing
- P https://kentcdodds.com/blog/stop-mocking-fetch
- P https://playwright.dev/docs/best-practices
- P https://fast-check.dev/docs/introduction/why-property-based/
- P https://docs.pact.io/
- S https://docs.rs/sqlx/latest/sqlx/attr.test.html (via search)
- downloaded, skimmed: https://testcontainers.com/guides/getting-started-with-testcontainers-for-nodejs/, https://docs.expo.dev/develop/unit-testing/, https://docs.maestro.dev/

## Error handling and crash reporting

- R https://www.lpalmieri.com/posts/error-handling-rust/
- P https://react.dev/reference/react/Component (componentDidCatch, getDerivedStateFromError)
- P https://docs.sentry.io/platforms/javascript/guides/react/features/error-boundary/
- P https://docs.sentry.io/platforms/javascript/data-management/sensitive-data/
- P https://doc.rust-lang.org/book/ch09-03-to-panic-or-not-to-panic.html

## Logging, observability, operations

- P https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html
- S https://stripe.com/blog/canonical-log-lines (summarized via fetch)
- P https://opentelemetry.io/docs/concepts/signals/traces/
- P https://opentelemetry.io/docs/concepts/context-propagation/
- P https://opentelemetry.io/docs/concepts/sampling/
- P https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/
- P https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/ (termination, grace period, preStop)
- P https://martinfowler.com/articles/feature-toggles.html (Pete Hodgson)
- R https://martinfowler.com/bliki/ParallelChange.html
- R https://martinfowler.com/bliki/BlueGreenDeployment.html
- R https://martinfowler.com/bliki/CanaryRelease.html

## Performance

- P https://web.dev/articles/vitals
- P https://web.dev/articles/performance-budgets-101
- P https://nodejs.org/en/learn/getting-started/profiling
- S clinic.js maintenance status (search: npm packages marked deprecated)

## Postmortems

- R https://blog.cloudflare.com/18-november-2025-outage/ (key sections)
- R https://blog.cloudflare.com/details-of-the-cloudflare-outage-on-july-2-2019/ (key sections)
- R https://status.cloud.google.com/incidents/ow5i3PPK96RduMcb1SsW (Google Cloud, 12 Jun 2025)
- R https://www.crowdstrike.com/wp-content/uploads/2024/08/Channel-File-291-Incident-Root-Cause-Analysis-08.06.2024.pdf (findings sections)
- R https://github.blog/news-insights/company-news/oct21-post-incident-analysis/ (key sections)
- R https://about.gitlab.com/blog/postmortem-of-database-outage-of-january-31/ (key sections)
- R https://aws.amazon.com/message/41926/ (S3, 28 Feb 2017)
- P https://engineering.fb.com/2021/10/05/networking-traffic/outage-details/
- S https://stripe.com/rcas/2019-07-10 (via search results; page not fetched)
- S https://www.sec.gov/newsroom/press-releases/2013-222 and SEC order 34-70694 (Knight Capital; PDF blocked, press release read)
- P https://github.com/danluu/post-mortems (README: Config, Time, Database sections)
