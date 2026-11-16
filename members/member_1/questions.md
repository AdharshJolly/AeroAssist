# Member 1 – Flight Information (`F01`–`F05`)

> **About this file:** the list of the five questions owned by Member 1 (Flight Information): for each one, the question text, the intent id and a few example phrasings the patterns should cover. Written and maintained only by this member.

Status: **implemented** in `flight_information.py`. Priority order: F05 → F02 → F01 → F03 → F04.

| ID | Intent | Example questions | Extracted |
|---|---|---|---|
| F01 | General Flight Status | How can I check my flight status? / How do I track my flight? | – |
| F02 | Specific Flight Status | What is the status of flight AI2025? / Is flight 6E123 on time? | `flight_code`, `airline_code`, `flight_number` |
| F03 | Flight Delay | What does a delayed flight mean? / My flight got delayed | – |
| F04 | Flight Cancellation | What happens if my flight gets cancelled? | – |
| F05 | Arrival Terminal | How can I find my arrival terminal for flight 6E123? | `flight_code` (optional) |

## Demo flight database
`FLIGHTS` in `flight_information.py` holds six made-up flights: AI2025, 6E123, SG456, QP1101, UK955, IX312. For these, F02 and F05 answer from the table (route, times, status, gate, arrival terminal) and end with "Demo data from a sample schedule, not live". Other flights get the generic "how to check" answer. Add a flight by adding one row to `FLIGHTS`.

| Try | Gives |
|---|---|
| status of flight 6E123 | delayed by 40 minutes, new departure 09:55 |
| which terminal will flight AI2025 arrive at? | Mumbai (BOM), Terminal 2, 08:40 |
| status of flight IX312 | cancelled, contact the airline |
| status of flight AI9999 | not in the table: how to check |

Flight numbers are written without a space (`AI2025`, `6E123`).
Full write-up: copy `docs/member_documentation_template.md` and fill it in.
