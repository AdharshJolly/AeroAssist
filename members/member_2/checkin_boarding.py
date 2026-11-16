"""checkin_boarding.py - Member 2: Check-in & Boarding (C01-C05).

WHAT THIS FILE DOES
  Defines INTENTS, a list of five intents. Each intent is a dictionary with:
    id        unique id (for example C01)
    name      short readable name (shown in the help screen and debug mode)
    patterns  list of regex strings, tried in order with re.search() and
              re.IGNORECASE; the first match wins
    response  the answer text; use {group_name} for values captured with
              named groups, or {group_name|default text} when optional
  Topics for this module: check-in procedures, web check-in, boarding passes, boarding times, missed check-in deadlines.

STATUS
  Every intent is a placeholder marked "active": False with no patterns, so
  the registry skips it and it can never match by accident.

HOW TO COMPLETE AN INTENT
  1. Write 2 or more regex variations inside "patterns".
  2. Write the "response" (never claim live data; qualify rules with
     "please confirm with your airline/airport").
  3. Delete the "active": False line.
  4. Fill in questions.md and try it: python main.py --debug
  Only edit THIS file and members/member_2/questions.md.

MATCHING ORDER
  Put specific intents before general ones, because the first match wins.
"""

INTENTS = [
    {
        "id": "C01",
        "name": "Check-in Procedure",
        # TODO (Member 2): write the user question this intent answers,
        #   then set "active" to True (or delete the line) when finished.
        "active": False,
        "patterns": [
            # TODO: add 2+ regex variations of the question, e.g.
            #   r"\bsome phrase\b",
            #   r"\balternative (?P<name>...) phrase\b",
        ],
        # TODO: add the response. Use {group_name} to insert extracted
        #   values, or {group_name|fallback text} for optional information.
        "response": "",
    },
    {
        "id": "C02",
        "name": "Web Check-in",
        # TODO (Member 2): write the user question this intent answers,
        #   then set "active" to True (or delete the line) when finished.
        "active": False,
        "patterns": [
            # TODO: add 2+ regex variations of the question, e.g.
            #   r"\bsome phrase\b",
            #   r"\balternative (?P<name>...) phrase\b",
        ],
        # TODO: add the response. Use {group_name} to insert extracted
        #   values, or {group_name|fallback text} for optional information.
        "response": "",
    },
    {
        "id": "C03",
        "name": "Boarding Pass",
        # TODO (Member 2): write the user question this intent answers,
        #   then set "active" to True (or delete the line) when finished.
        "active": False,
        "patterns": [
            # TODO: add 2+ regex variations of the question, e.g.
            #   r"\bsome phrase\b",
            #   r"\balternative (?P<name>...) phrase\b",
        ],
        # TODO: add the response. Use {group_name} to insert extracted
        #   values, or {group_name|fallback text} for optional information.
        "response": "",
    },
    {
        "id": "C04",
        "name": "Boarding Time",
        # TODO (Member 2): write the user question this intent answers,
        #   then set "active" to True (or delete the line) when finished.
        "active": False,
        "patterns": [
            # TODO: add 2+ regex variations of the question, e.g.
            #   r"\bsome phrase\b",
            #   r"\balternative (?P<name>...) phrase\b",
        ],
        # TODO: add the response. Use {group_name} to insert extracted
        #   values, or {group_name|fallback text} for optional information.
        "response": "",
    },
    {
        "id": "C05",
        "name": "Missed Check-in Deadline",
        # TODO (Member 2): write the user question this intent answers,
        #   then set "active" to True (or delete the line) when finished.
        "active": False,
        "patterns": [
            # TODO: add 2+ regex variations of the question, e.g.
            #   r"\bsome phrase\b",
            #   r"\balternative (?P<name>...) phrase\b",
        ],
        # TODO: add the response. Use {group_name} to insert extracted
        #   values, or {group_name|fallback text} for optional information.
        "response": "",
    },
]
