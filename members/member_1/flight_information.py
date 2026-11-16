"""flight_information.py - Member 1: Flight Information (F01-F05).

WHAT THIS FILE DOES
  Defines INTENTS, the five flight questions the chatbot can answer:
    F05 Arrival Terminal        "which terminal will flight 6E123 arrive at?"
    F02 Specific Flight Status  "what is the status of flight AI2025?"
    F01 General Flight Status   "how can I check my flight status?"
    F03 Flight Delay            "what does a delayed flight mean?"
    F04 Flight Cancellation     "what happens if my flight gets cancelled?"
  Each intent has several regex patterns (matched with re.search() and
  re.IGNORECASE) and a response template.

ORDER MATTERS
  The engine stops at the first match, so specific intents (those that need
  a flight number) come BEFORE general ones: F05 -> F02 -> F01 -> F03 -> F04.

HOW FLIGHT NUMBERS ARE HANDLED
  FLIGHT_CODE uses nested named groups to split "6E123" into
  airline_code ("6E") and flight_number ("123"); flight_code holds the whole
  thing. Flight numbers must be written WITHOUT a space (AI2025, not
  AI 2025) so ordinary text like "is 30 minutes" is not mistaken for one.

DYNAMIC RESPONSES
  Captured groups ({flight_code}, {airline_code}, {flight_number}) are
  inserted into the answers. Optional ones use a default ({flight_code|your flight}).

NAMING THE AIRLINE
  AIRLINES (below) maps a prefix to an airline name. At the bottom of the file
  a small loop copies F05 and F02 once per airline (ids like "F02-6E"), with
  the prefix written into the patterns and the name written into the response
  ("Open IndiGo's app"). The original F05/F02 stay right after their copies as
  the fallback for unknown prefixes ("Open your airline's app").
  The table is general knowledge, NOT live data, and can go out of date.

HONESTY RULE
  Responses never claim live flight data. They explain how to check, what to
  do next, and ask the passenger to confirm with the airline.
"""

# Airline prefix -> airline name. Static, NOT live data; airlines merge or stop
# flying, so check it from time to time.
AIRLINES = {
    "AI": "Air India",
    "IX": "Air India Express",
    "6E": "IndiGo",
    "SG": "SpiceJet",
    "QP": "Akasa Air",
    "9I": "Alliance Air",
    "UK": "Air India",  # Vistara merged into Air India; UK flights now run under Air India
}

# A flight code = airline code + 2 to 4 digits, e.g. AI2025, 6E123, UK955.
# Nested named groups split it:  flight_code = airline_code + flight_number
#   (?:[A-Z]{2}|\d[A-Z]|[A-Z]\d)  two letters (AI), digit+letter (6E) or letter+digit (G8)
#   \d{2,4}                       then 2 to 4 digits
#   \b ... \b                     whole token only (no AI20255, no xAI2025)
ANY_AIRLINE_CODE = r"(?:[A-Z]{2}|\d[A-Z]|[A-Z]\d)"
FLIGHT_CODE = (
    r"\b(?P<flight_code>(?P<airline_code>" + ANY_AIRLINE_CODE + r")"
    r"(?P<flight_number>\d{2,4}))\b"
)

# "flight AI2025", "flight number AI2025", "flight no. AI2025"
FLIGHT_REF = r"\bflight\s+(?:(?:number|no\.?|code)\s+)?" + FLIGHT_CODE

_BASE_INTENTS = [
    # ------------------------------------------------------------------ F05
    {
        "id": "F05",
        "name": "Arrival Terminal",
        "patterns": [
            # "arrival terminal for flight 6E123"
            r"\b(?:arrival|arriving)\s+terminal\b.*?" + FLIGHT_REF,
            # "which terminal will flight 6E123 arrive at?"  ((?=...) = look-ahead)
            r"(?=.*\b(?:arriv\w*|land\w*)\b)\bterminal\b.*?" + FLIGHT_REF,
            # "flight 6E123 arrives at which terminal?"
            FLIGHT_REF + r".*\b(?:arriv\w*|land\w*)\b.*\bterminal\b",
            # No flight number given (optional information)
            r"\b(?:arrival|arriving)\s+terminal\b",
            r"\bwhich\s+terminal\b.*\b(?:arriv\w*|land\w*)\b",
        ],
        "response": (
            "Looking for the arrival terminal of {flight_code|your flight}? "
            "I do not have live flight data, so I cannot tell you the actual terminal. "
            "Here is how to find it:\n"
            "1. Check your booking confirmation or e-ticket; some airlines print the "
            "terminal there.\n"
            "2. Open {airline|your airline}'s app or website and look under flight status.\n"
            "3. Look at the arrivals display screens once you reach the airport.\n"
            "4. Ask airline staff or the airport information desk.\n"
            "At airports with several terminals the terminal can depend on the airline "
            "and may change, so confirm close to your travel date."
        ),
    },
    # ------------------------------------------------------------------ F02
    {
        "id": "F02",
        "name": "Specific Flight Status",
        "patterns": [
            # "status of flight AI2025", "details about flight AI2025"
            r"\b(?:status|updates?|information|info|details?)\b.{0,25}?" + FLIGHT_REF,
            # "how can I check my flight status for 6E123" (no word "flight" before the code)
            r"\b(?:status|updates?|information|info|details?)\b.{0,25}?\b(?:for|of|on)\s+" + FLIGHT_CODE,
            # "check flight AI2025", "is flight AI2025 on time", "where is my flight AI2025"
            r"\b(?:check|track|is|has)\s+(?:my\s+)?" + FLIGHT_REF,
            # "flight AI2025 status", "flight AI2025 delayed?"
            FLIGHT_REF + r".*\b(?:status|delayed|on time|cancell?ed|departed|landed)\b",
            # just "flight AI2025"
            r"^\W*" + FLIGHT_REF + r"\W*$",
        ],
        "response": (
            "You are enquiring about flight {flight_code}. The airline prefix is "
            "{airline_code} and the flight number is {flight_number}. "
            "I cannot access live flight information, so I cannot confirm its status. "
            "To check it:\n"
            "1. Open {airline|your airline}'s app or website, choose Flight Status and "
            "enter {flight_number} with your travel date.\n"
            "2. Look for the flight on the display screens at the airport.\n"
            "3. Watch for SMS or email alerts from the airline.\n"
            "4. Still unsure? Ask at the airline's counter or call its helpline.\n"
            "Keep your booking reference (PNR) handy."
        ),
    },
    # ------------------------------------------------------------------ F01
    {
        "id": "F01",
        "name": "General Flight Status",
        "patterns": [
            # "How can I check my flight status?"
            r"\b(?:check|track|know|find|see|get)\b.*\bflight\s+(?:status|information|info|details)\b",
            # "How do I track my flight?"
            r"\bhow\b.*\b(?:track|monitor|follow)\b.*\bflight\b",
            # "How do I know if my flight is on time?"
            r"\bhow\b.*\bflight\b.*\b(?:on time|on schedule)\b",
            # just "flight status?"
            r"^\W*(?:the\s+)?flight\s+status\W*$",
        ],
        "response": (
            "I cannot show live flight status myself, but you can check it like this:\n"
            "1. Airline app or website: enter your flight number (for example AI2025) "
            "and travel date, or your booking reference (PNR).\n"
            "2. Airport display screens: find your flight in the departures list.\n"
            "3. SMS or email alerts: airlines send these to the contact details on your "
            "booking.\n"
            "4. Airline helpline or counter: ask them if the other sources disagree.\n"
            "Tip: tell me your flight number (e.g. 'status of flight 6E123') and I will "
            "show you where to look for that airline."
        ),
    },
    # ------------------------------------------------------------------ F03
    {
        "id": "F03",
        "name": "Flight Delay",
        "patterns": [
            # "What does a delayed flight mean?"
            r"\bwhat\b.*\bdelay(?:ed|s)?\b.*\bmeans?\b",
            # "What does it mean when my flight is delayed?"
            r"\bmeans?\b.*\bflight\b.*\bdelayed\b",
            # "My flight got delayed", "flight delays", "delay of my flight"
            r"\b(?:flight\b.*\bdelay(?:ed|s)?|delay(?:ed|s)?\b.*\bflight)\b",
        ],
        "response": (
            "A delayed flight is one that departs or arrives later than its scheduled "
            "time. Common reasons include weather, air traffic congestion, technical "
            "checks or a late incoming aircraft. What you are entitled to (such as "
            "meals or rebooking) depends on the airline and the length of the delay, "
            "so please confirm with your airline.\n"
            "What to do now:\n"
            "1. Check the revised time on the airline app, SMS or display screens.\n"
            "2. Stay within reach of your gate and listen for announcements.\n"
            "3. Ask airline staff about meals or refreshments if the delay is long.\n"
            "4. If it is very long, ask about rebooking or a refund.\n"
            "Keep your boarding pass and booking confirmation with you."
        ),
    },
    # ------------------------------------------------------------------ F04
    {
        "id": "F04",
        "name": "Flight Cancellation",
        "patterns": [
            # "What happens if my flight gets cancelled?"
            r"\bwhat\b.*\b(?:happens?|do|should|if)\b.*\bcancell?(?:ed|ation)s?\b",
            # "my flight is cancelled", "flight cancellation", "cancelled flight"
            r"\b(?:flight\b.*\bcancell?(?:ed|ation)s?|cancell?(?:ed|ation)s?\b.*\bflight)\b",
        ],
        "response": (
            "If your flight is cancelled, your airline should inform you by SMS, email "
            "or app. What you are entitled to depends on the airline's policy and the "
            "reason for the cancellation, so please confirm the details with your "
            "airline.\n"
            "What to do now:\n"
            "1. Read the airline's SMS, email or app message for the next steps.\n"
            "2. Go to the airline counter or call its helpline and ask for the next "
            "available flight or a refund.\n"
            "3. Keep your booking confirmation, boarding pass and any messages received.\n"
            "4. If you booked through a travel app or agent, contact them as well."
        ),
    },
]


def _copy_per_airline(intent):
    """One copy of `intent` per airline: prefix fixed in the patterns, name fixed in the response."""
    copies = []
    for code, name in AIRLINES.items():
        patterns = [p.replace(ANY_AIRLINE_CODE, code) for p in intent["patterns"]
                    if ANY_AIRLINE_CODE in p]  # patterns without a flight number need no copy
        copies.append({
            "id": f"{intent['id']}-{code}",
            "name": intent["name"],
            "patterns": patterns,
            "response": intent["response"].replace("{airline|your airline}", name),
        })
    return copies


# Airline-specific copies go BEFORE their generic intent (first match wins).
INTENTS = []
for _intent in _BASE_INTENTS:
    if _intent["id"] in ("F05", "F02"):
        INTENTS += _copy_per_airline(_intent)
    INTENTS.append(_intent)
