"""checkin_boarding.py - Member 2: Check-in & Boarding (C01-C05).

WHAT THIS FILE DOES
  Defines INTENTS, the five check-in and boarding questions the chatbot can answer:
    C05 Missed Check-in Deadline  "what happens if I miss my check-in deadline?"
    C02 Web Check-in              "how can I complete web check-in?"
    C03 Boarding Pass             "what is a boarding pass?"
    C04 Boarding Time             "when does boarding usually begin?"
    C01 Check-in Procedure        "how early should I reach the airport?"
  Each intent is a dictionary with:
    id        unique id
    name      short readable name (shown in the help screen and debug mode)
    patterns  list of regex strings, tried in order with re.search() and
              re.IGNORECASE; the first match wins
    response  the answer text; {group_name} is replaced by a value captured
              with a named group, {group_name|default} uses the default text
              when that optional group did not match

ORDER MATTERS
  The engine stops at the first match, so the more SPECIFIC intents come
  BEFORE the general ones. Priority here:  C05 -> C02 -> C03 -> C04 -> C01.
  (C01 is last because its words "airport" and "check-in" appear in many
  other questions.)  Member 1's flight intents are checked before all of these.

NAMED GROUPS USED (all optional, every one has a default in the response)
  cutoff_type  C05  deadline / cut-off / time / counter
  mode         C02  web / online / mobile / digital / app
  airline      C02  only a known airline name (IndiGo, Air India, ...), so
                    words like "my flight" are never mistaken for an airline
  pass_type    C03  digital / mobile / printed / paper
  flight_type  C04, C01  domestic / international
  action       C01  reach / arrive at / get to / be at

HONESTY RULE
  Responses give general, typical timings only ("typically", "usually") and
  always ask the passenger to confirm with the airline/airport. They never
  claim live information.
"""

# Regex pieces used in the patterns below:
#   \b            word boundary, so "late" does not match inside "relate"
#   check[- ]?in  "check-in", "check in" and "checkin" (the [- ]? is an optional
#                 hyphen or space)
#   .*            any text in between, so the key words can be far apart
#   (?:a|b)       alternation without capturing (just "a or b")
#   (?P<x>...)    named capturing group, available as {x} in the response
#   (...)?        optional part (the group may not match; the default is used)
#   \s+           one or more spaces
#   s?  e?        optional ending letters (starts / start, passes / pass)

INTENTS = [
    # ------------------------------------------------------------------ C05
    {
        "id": "C05",
        "name": "Missed Check-in Deadline",
        # User question: What happens if I miss my check-in deadline?
        "patterns": [
            # "I missed my check-in", "late for check-in deadline", "miss the check-in cut-off"
            # The optional group captures what was missed (deadline / cut-off / time / counter).
            r"\b(?:miss(?:ed)?|late\s+for)\b.*\bcheck[- ]?in(?:\s+(?P<cutoff_type>deadline|cut[- ]?off|time|counter))?\b",
            # "check-in deadline passed", "check-in closed", "check-in cut off"
            r"\bcheck[- ]?in\b.*\b(?P<cutoff_type>deadline|cut[- ]?off|close[sd]?|late|miss(?:ed)?)\b",
            # "what to do if I am late for check-in"
            r"\b(?:what\s+happens|what\s+to\s+do)\b.*\b(?:miss(?:ed)?|late)\b.*\bcheck[- ]?in\b",
        ],
        "response": (
            "If you miss the check-in {cutoff_type|deadline} (typically 45-60 minutes before "
            "domestic departure and 60-75 minutes for international flights), the flight manifest "
            "closes and boarding is not permitted. Please contact your airline's ticketing counter "
            "immediately for rebooking options, and please confirm specific policies with your airline/airport."
        ),
    },
    # ------------------------------------------------------------------ C02
    {
        "id": "C02",
        "name": "Web Check-in",
        # User question: How can I complete web check-in?
        "patterns": [
            # "web check-in", "online check-in for IndiGo", "mobile check in"
            # mode = web/online/...; airline is captured ONLY when it is one of the
            # listed airline names (a fixed alternation), never arbitrary words.
            r"\b(?P<mode>web|online|mobile|digital|app)\s*check[- ]?in\b(?:.*\bfor\s+(?P<airline>indigo|air\s+india(?:\s+express)?|spicejet|akasa(?:\s+air)?|vistara|alliance\s+air)\b)?",
            # "how do I complete check-in", "how can I finish online check in"
            r"\bhow\b.*\b(?:complete|do|finish)\b.*\b(?P<mode>web|online|mobile)?\s*check[- ]?in\b",
            # "check-in online", "check in via app"
            r"\bcheck[- ]?in\s+(?P<mode>online|on\s+the\s+web|via\s+app)\b",
        ],
        "response": (
            "You can complete {mode|online} check-in (typically 24 to 48 hours before departure) by "
            "visiting the website or mobile app of {airline|your airline}, entering your PNR/Booking "
            "Reference and Last Name, selecting your seat, and downloading your boarding pass. "
            "Timings vary, so please confirm with your airline/airport."
        ),
    },
    # ------------------------------------------------------------------ C03
    {
        "id": "C03",
        "name": "Boarding Pass",
        # User question: What is a boarding pass?
        "patterns": [
            # "what is a boarding pass", "explain digital boarding pass"
            r"\b(?:what\s+is|what's|explain|define)\b.*\b(?:(?P<pass_type>digital|mobile|printed|paper|e-?)\s+)?boarding\s+pass(?:es)?\b",
            # "why do I need a boarding pass", "how to get a printed boarding pass"
            r"\b(?:why\s+do\s+i\s+need|how\s+to\s+get)\b.*\b(?:(?P<pass_type>digital|mobile|printed|paper)\s+)?boarding\s+pass(?:es)?\b",
            # just "boarding pass" or "digital boarding pass" (broadest, so it is last)
            r"\b(?:(?P<pass_type>digital|mobile|printed|paper)\s+)?boarding\s+pass(?:es)?\b",
        ],
        "response": (
            "A {pass_type|printed or digital} boarding pass is an official document issued during "
            "check-in that grants you permission to pass security screening and board the aircraft. "
            "It displays your passenger name, flight number, seat number, gate, and boarding time. "
            "For specific digital pass acceptance rules, please confirm with your airline/airport."
        ),
    },
    # ------------------------------------------------------------------ C04
    {
        "id": "C04",
        "name": "Boarding Time",
        # User question: When does boarding usually begin?
        "patterns": [
            # "when does boarding begin for international flights"
            r"\b(?:when|what\s+time|how\s+early)\b.*\bboarding\b.*\b(?:begin|start|open)s?\b(?:.*\bfor\s+(?P<flight_type>domestic|international)\s+flights?)?",
            # "boarding time", "boarding gate closes", "boarding schedule domestic"
            r"\bboarding\b.*\b(?:begin|start|open|time|schedule|gate)s?\b(?:.*\b(?P<flight_type>domestic|international))?",
            # "when should I board", "what time can we board"
            r"\b(?:when|what\s+time)\b.*\b(?:can|should|must|do|will)\s+(?:i|we)\s+board\b(?:.*\b(?P<flight_type>domestic|international))?",
        ],
        "response": (
            "For {flight_type|domestic and international} flights, boarding usually begins 45 to 60 "
            "minutes before scheduled departure, and boarding gates strictly close 15 to 20 minutes "
            "before takeoff. Because gate schedules can change, please confirm with your airline/airport."
        ),
    },
    # ------------------------------------------------------------------ C01
    {
        "id": "C01",
        "name": "Check-in Procedure",
        # User question: How early should I reach the airport?
        "patterns": [
            # "how early should I reach the airport", "what time should I be at the airport"
            # action = the verb the user used, so the answer repeats it ("arrive at", "get to").
            r"\b(?:how\s+early|when|how\s+soon|what\s+time|hours?\s+before)\b.*\b(?P<action>reach|arrive\s+at|get\s+to|be\s+at)\b.*\bairport\b(?:.*\b(?P<flight_type>domestic|international))?",
            # "reach the airport", "arrive at the airport for an international flight"
            r"\b(?P<action>reach|arrive\s+at)\b.*\bairport\b(?:.*\b(?P<flight_type>domestic|international)\s+flight)?",
            # "airport arrival", "check-in procedure"
            r"\b(?:airport\s+arrival|check[- ]?in\s+procedure)\b(?:.*\b(?P<flight_type>domestic|international))?",
            # "what time does the check-in counter open?"
            r"\bcheck[- ]?in\s+counters?\b.*\b(?:open|start|begin)s?\b(?:.*\b(?P<flight_type>domestic|international))?",
        ],
        "response": (
            "To complete airport check-in procedures smoothly for {flight_type|your} flight, you "
            "should {action|reach} the airport at least 2 hours before domestic departures and "
            "3 to 4 hours before international departures. Please confirm exact counter opening "
            "times with your airline/airport."
        ),
    },
]
