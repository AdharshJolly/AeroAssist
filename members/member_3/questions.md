# Member 3 – Baggage Assistance (`B01`–`B05`)

> **About this file:** the list of the five questions owned by Member 3 (Baggage Assistance): for each one, the question text, the intent id and a few example phrasings the patterns should cover. Written and maintained only by this member.

Status: **implemented** in `baggage_assistance.py`. Priority order: B05 → B04 → B03 → B01 → B02.

| ID | Intent | Example questions | Extracted |
|---|---|---|---|
| B01 | Cabin Baggage Allowance | What is the cabin baggage allowance? / How much hand luggage can I carry? / How many bags can I take in the cabin? / What is the hand baggage limit? / Is carry-on size limited? | – |
| B02 | Check-in Baggage Allowance | What is the check-in baggage allowance? / How much luggage can I check in? / What is the maximum weight for checked baggage? / How many kilos of luggage can I check? / How many kg can I take? / What is the excess baggage fee? / My bag is overweight | – |
| B03 | Laptop and Electronics | Can I carry a laptop in my cabin baggage? / Is a laptop allowed in hand luggage? / Can I take my laptop on the flight? / Can I take a camera on the flight? | – |
| B04 | Liquid Restrictions | Can I carry liquids in my hand luggage? / How much liquid can I take on a flight? / Are liquids allowed in cabin baggage? / Can I bring water in my bag? | – |
| B05 | Lost Baggage | What should I do if my luggage is lost? / What if my checked baggage is missing? / My suitcase did not arrive / I can't find my bag / My bag is damaged / How can I report missing baggage? | – |

## Why this order
The first match wins, so specific intents come first. "Can I carry a laptop in my cabin baggage?" mentions cabin baggage (B01) but is about a laptop, so B03 is checked before B01. B02 is last because it also catches general questions such as "how many kg can I take?".

## Not covered (gets the default reply)
Lost and found, and anything outside the five topics. "I lost my boarding pass in my bag" is deliberately not treated as lost baggage. Add a new intent if you want them.

Full write-up: copy `docs/member_documentation_template.md` and fill it in.
