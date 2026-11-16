# Member 2 – Check-in & Boarding (`C01`–`C05`)

> **About this file:** the list of the five questions owned by Member 2 (Check-in & Boarding): for each one, the question text, the intent id and a few example phrasings the patterns cover. Written and maintained only by this member.

Status: **implemented** in `checkin_boarding.py`.

| ID | Intent | Question | Alternative phrasing | Extracted info (named groups) |
|---|---|---|---|---|
| C01 | Check-in Procedure | How early should I reach the airport? | When should I get to the airport?; what time should I be at the airport; what time does the check-in counter open? | `action`, `flight_type` |
| C02 | Web Check-in | How can I complete web check-in? | online check-in for IndiGo; mobile check-in | `mode`, `airline` (known airline names only) |
| C03 | Boarding Pass | What is a boarding pass? | what is a digital boarding pass; boarding pass | `pass_type` |
| C04 | Boarding Time | When does boarding usually begin? | when should I board; boarding time for international flights | `flight_type` |
| C05 | Missed Check-in Deadline | What happens if I miss my check-in deadline? | I am late for check-in; check-in closed | `cutoff_type` |

Match order (first match wins): C05 → C02 → C03 → C04 → C01.
