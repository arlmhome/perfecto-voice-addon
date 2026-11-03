# Perfecto Voice — broker prototype

This add-on creates short-lived OpenAI Realtime client secrets without exposing the long-lived API key in dashboard JavaScript.

**Status:** Prototype, not deployed. No Home Assistant device control, wake word, or WebRTC browser client is included in this commit.

## Installation planning
The directory is a Home Assistant add-on source, not yet a configured add-on repository. It must be packaged/registered with the HA add-on manager before installation. Store the API key only in add-on options. Do not commit it.

## Security
Ingress-only: no external port mapping. The broker does not accept Home Assistant service calls. Session secrets are returned only to authenticated ingress clients; browser integration must use the authenticated ingress URL, not a public direct endpoint.

## Smoke checks
GET /health returns key_configured (no secret); POST /session requests a short-lived Realtime secret. Validate upstream schema and add-on build before enabling this in Test.
