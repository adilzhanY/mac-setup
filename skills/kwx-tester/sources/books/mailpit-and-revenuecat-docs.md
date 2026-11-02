# Mailpit and RevenueCat testing docs

- Authors: Ralph Slooten (Mailpit); RevenueCat
- Year: read 2026-10-31 (Mailpit 1.33)
- Legal URL: https://mailpit.axllent.org/docs/install/docker/ ; https://mailpit.axllent.org/docs/api-v1/ ; https://github.com/axllent/mailpit (swagger.json) ; https://www.revenuecat.com/docs/test-and-launch/sandbox ; https://www.revenuecat.com/docs/test-and-launch/sandbox/google-play-store

## What I read

Mailpit Docker install page, API overview and the swagger file paths; RevenueCat sandbox overview and the Google Play sandbox page.

## Key lessons used in backend/external-services-and-time.md

- Mailpit: SMTP 1025, UI and API 8025; `GET /api/v1/messages`, `GET /api/v1/search?query=`, `GET /api/v1/message/latest`, `DELETE /api/v1/messages`.
- RevenueCat Test Store first, platform sandboxes before review; sandbox prices unreliable.
- Google Play test subscriptions renew in 5 to 30 minutes and at most six times; license testers in Play Console.
