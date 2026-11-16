"""baggage_assistance.py - Member 3: Baggage Assistance (B01-B05).

WHAT THIS FILE DOES
  Defines INTENTS, a list of five intents. Each intent is a dictionary with:
    id        unique id (for example B01)
    name      short readable name (shown in the help screen and debug mode)
    patterns  list of regex strings, tried in order with re.search() and
              re.IGNORECASE; the first match wins
    response  the answer text; use {group_name} for values captured with
              named groups, or {group_name|default text} when optional
  Topics for this module: cabin and check-in baggage allowance, laptops, liquids, lost baggage.

STATUS
  Every intent is a placeholder marked "active": False with no patterns, so
  the registry skips it and it can never match by accident.

HOW TO COMPLETE AN INTENT
  1. Write 2 or more regex variations inside "patterns".
  2. Write the "response" (never claim live data; qualify rules with
     "please confirm with your airline/airport").
  3. Delete the "active": False line.
  4. Fill in questions.md and try it: python main.py --debug
  Only edit THIS file and members/member_3/questions.md.

MATCHING ORDER
  Put specific intents before general ones, because the first match wins.
"""

INTENTS = [
    {
        "id": "B01",
        "name": "Cabin Baggage Allowance",
        # TODO (Member 3): write the user question this intent answers,
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
        "id": "B02",
        "name": "Check-in Baggage Allowance",
        # TODO (Member 3): write the user question this intent answers,
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
        "id": "B03",
        "name": "Laptop Transportation",
        # TODO (Member 3): write the user question this intent answers,
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
        "id": "B04",
        "name": "Liquid Restrictions",
        # TODO (Member 3): write the user question this intent answers,
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
        "id": "B05",
        "name": "Lost Baggage",
        # TODO (Member 3): write the user question this intent answers,
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
