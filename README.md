# AeroAssist – Your Virtual Airport Assistance Desk

> **About this file:** the front page of the project. It explains what AeroAssist is, how to run it, how the folders are organised, how the chatbot picks an answer, and the exact steps a team member follows to add their five questions. Read this first.

A rule-based NLP chatbot for Indian airport passenger assistance, built with Python's `re` module only (university NLP CIA project).

## Problem statement
First-time flyers often struggle with airport procedures: flight information, check-in, baggage rules, security screening, boarding and facilities. AeroAssist answers these general questions in a command-line conversation. It identifies the question with regular expressions, extracts details (e.g. a flight number) with capturing groups and fills them into predefined responses.

It gives **general guidance only**. It has no live flight data and never claims to; baggage/security answers should be confirmed with the airline or airport. For demonstration, Member 1 also keeps a small **demo flight database** (made-up sample flights); answers from it always say they are demo data.

## Features
- Intent detection with `re.search()`; greetings, help and exit with `re.match()`
- Text cleaning with `re.sub()`; several questions in one message with `re.split()`
- Named capturing groups → dynamic responses (`{flight_code}`)
- Four independent member modules, validated at startup with clear error messages
- `--debug` mode showing matched intent id and module
- Demo flight database: sample flights (`AI2025`, `6E123`, ...) get route, times, status, gate and terminal
- Standard library only, Python 3.10+

## Run
```bash
python main.py            # normal chat
python main.py --debug    # also show intent id, module, extracted groups
```
No installation needed (`requirements.txt` lists no packages).

## Directory structure
```
AeroAssist/
├── main.py                  CLI loop and banner
├── chatbot/
│   ├── config.py            branding, fixed messages, greeting/help/exit patterns
│   ├── preprocessor.py      re.sub + re.split → list of queries
│   ├── registry.py          imports + validates all members' INTENTS
│   ├── engine.py            matching and response generation (no domain regex)
│   └── response_handler.py  template filling, wrapping, help text
└── members/member_1..4/     one module + questions.md per member

```

## How the chatbot works
1. `main.py` reads a line and calls `engine.respond(text)`.
2. `preprocess()` cleans the text and splits it into separate queries (`?`, `;`, new line).
3. For each query the engine first checks greeting / help / exit (`re.match`).
4. Otherwise it tries every intent's patterns in order with `re.search`, case-insensitively. **First match wins.**
5. Named groups are extracted, cleaned (`*_code` groups are upper-cased) and substituted into the response template.
6. No match → the default "I'm sorry, I couldn't understand your query…" message.

### Matching priority
Order = Member 1 → 4, then the order of each member's `INTENTS` list, then the order of each intent's `patterns`. Put **specific intents before general ones** (Member 1 does: `F05 → F02 → F01 → F03 → F04`). Avoid broad patterns; the registry rejects any pattern that matches empty text.

### Response templates
- `{flight_code}` – replaced by the named group; the pattern **must** define `(?P<flight_code>…)` in every pattern of that intent (checked at startup).
- `{flight_code|your flight}` – optional information; the text after `|` is used when the group did not match.

### Demo flight database (Member 1)
`FLIGHTS` in `members/member_1/flight_information.py` is a small dictionary of made-up flights. Asking about a flight in it (F02 status, F05 arrival terminal) gives real details from the table; the answer ends with "Demo data from a sample schedule, not live". Flights not in the table get the generic "how to check" answer. To add a flight, add one row to `FLIGHTS`:
```python
"AI2025": {"from": "Delhi (DEL)", "to": "Mumbai (BOM)", "dep": "06:30", "arr": "08:40",
           "status": "On time", "note": "", "gate": "12", "arr_terminal": "Terminal 2"},
```
Try: `status of flight 6E123`, `which terminal will flight AI2025 arrive at?`, `status of flight IX312` (cancelled).

### Baggage questions (Member 3)
Member 3's five intents are checked in the order B05 → B04 → B03 → B01 → B02, so the specific ones win (a laptop question is B03 even if it says "cabin baggage").

| ID | Intent | Try |
|---|---|---|
| B01 | Cabin Baggage Allowance | `What is the cabin baggage allowance?` / `is carry-on size limited` |
| B02 | Check-in Baggage Allowance | `How much luggage can I check in?` / `what is the excess baggage fee` |
| B03 | Laptop and Electronics | `Can I carry a laptop in my cabin baggage?` |
| B04 | Liquid Restrictions | `Can I carry liquids in my hand luggage?` / `can I bring water in my bag` |
| B05 | Lost Baggage | `What should I do if my luggage is lost?` / `my bag is damaged` |

Answers are general guidance only; confirm with your airline.

## How each member adds their five questions
You only edit **your own** files: `members/member_N/<module>.py`, `members/member_N/questions.md`.

1. Open your module. Each placeholder intent has `"active": False` and empty `patterns`.
2. For one intent: write 2+ regex variations in `patterns`, write the `response`, and **delete the `"active": False` line**.
3. Use named groups for values you want to show, e.g. `(?P<weight>\d{1,2})\s*kg`, then `{weight}` in the response.
4. Try your questions live: `python main.py --debug`.

Intent schema:
```python
{
    "id": "F02",                       # unique
    "name": "Specific Flight Status",
    "patterns": [r"\bstatus of flight (?P<flight_code>[A-Z]{2}\d{2,4})\b"],
    "response": "You are enquiring about flight {flight_code}. ...",
    # "active": False                  # placeholder only; remove when finished
}
```
If your pattern or template is invalid, `python main.py` stops with a message naming your member, intent id and pattern.

## Sample conversation
```
You: What is the status of flight AI2025?

AeroAssist:
You are enquiring about flight AI2025. I cannot access live flight
information, so I cannot confirm its status. Please check your
airline's official website or app, ...

You: what happens if my flight gets cancelled?; arrival terminal for flight 6e123
(two answers, one per question)
```

## Project status
- Member 1: implemented (F01–F05).
- Member 2: implemented (C01–C05).
- Member 3: implemented (B01–B05).
- Member 4: placeholders (S01–S05), inactive until completed.
