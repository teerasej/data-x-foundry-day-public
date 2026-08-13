# Fabrikam Service Operations Handbook

This synthetic handbook is for workshop use only. It does not describe a real company or production process.

## Incident priority and acknowledgement

- **P1 — Critical:** A customer-facing service is unavailable for all or most users, or there is a confirmed security incident. Acknowledge within **15 minutes** and start human escalation immediately.
- **P2 — High:** A major feature is degraded, but a practical workaround exists. Acknowledge within **30 minutes** and assign a service owner.
- **P3 — Standard:** A limited defect, information request, or planned service request. Acknowledge within **4 business hours**.

## Human escalation

Escalate immediately for P1 incidents, suspected security or privacy exposure, duplicate financial charges, legal requests, and any case where the evidence is insufficient for a safe automated response. The AI assistant may recommend escalation but must not contact a real person or modify a production ticket.

## Planned maintenance

The synthetic maintenance window is Tuesday and Thursday from **22:00 to 23:00 ICT**. Notify affected users at least two business days before planned work. Emergency maintenance requires approval from the on-duty service owner.

## Data handling

Use only synthetic workshop data in AI tools. Do not enter passwords, access tokens, personal data, tenant identifiers, subscription identifiers, or production incident details. When a request contains sensitive data, stop automated processing and ask for human review.
