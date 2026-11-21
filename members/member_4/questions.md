# Member 4 – Security & Airport Facilities (`S01`–`S05`)

> **About this file:** the list of the five questions owned by Member 4 (Security & Facilities): for each one, the question text, the intent id and a few example phrasings the patterns should cover. Written and maintained only by this member.

Status: **implemented** in `security_facilities.py`.

| ID | Intent | Example questions | Extracted |
|---|---|---|---|
| S01 | Domestic Travel Documents | What documents do I need for a domestic flight? / Can I travel domestically with Aadhaar? / Is PAN card accepted for domestic flights? | `document` |
| S02 | Security Screening | What happens during airport security check? / What items are prohibited at airport security? / Are knives allowed in cabin baggage? | `item` |
| S03 | Power Bank Transportation | Can I carry a power bank on a flight? / What is the power bank limit? / Can I put my power bank in checked baggage? | `capacity` |
| S04 | Wheelchair Assistance | How can I request wheelchair assistance? / I need wheelchair assistance at the airport | `assistance` |
| S05 | Lost and Found | Where is the lost and found? / I lost my phone at the airport / I cannot find my passport | `item` |

## Note on Member 3
Member 3 is checked first. Its patterns skip power bank and prohibited-item questions so they reach S02 and S03.

Full write-up: copy `docs/member_documentation_template.md` and fill it in.
