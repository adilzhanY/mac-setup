# Pact documentation

- Author: Pact Foundation
- Year: living documentation, read 2026-10-31 (Pact JS 17.1)
- Legal URL: https://docs.pact.io/getting_started/what_is_pact_good_for ; https://docs.pact.io/getting_started/how_pact_works ; https://docs.pact.io/pact_broker/can_i_deploy ; https://docs.pact.io/implementation_guides/javascript/docs/consumer ; https://docs.pact.io/implementation_guides/javascript/docs/provider

## What I read

What Pact is good for, how Pact works, can-i-deploy, Pact JS consumer and provider guides.

## Key lessons used in backend/contract-and-schema-testing.md

- Good for integrations where you control both sides; poor fit for public APIs, pass-through APIs, functional testing, load testing, uncontrolled providers.
- Consumer tests against a mock provider write the pact; the provider replays it; provider states set preconditions.
- Without `stateHandlers`, the Verifier ignores states and only warns.
- Publish verification results from CI with the git SHA; `can-i-deploy` and `record-deployment` gate releases.
- V4 builder API: `addInteraction().given().uponReceiving().withRequest().willRespondWith().executeTest()`.
