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
  All five intents are active and contain regex patterns and responses.

MATCHING ORDER
  The first match wins, so the SPECIFIC intents come first:
    B05 Lost Baggage -> B04 Liquids -> B03 Laptop -> B01 Cabin -> B02 Check-in
  Example: "can I carry a laptop in my cabin baggage?" mentions cabin baggage
  (B01) but is really about a laptop (B03), so B03 is checked before B01.
  B02 is last and also catches general questions ("how many kg can I take?").

PATTERN STYLE
  Every pattern is a keyword pattern (no whole sentences), so many different
  phrasings of the same question match:
    (?:a|b)    "a or b" without capturing        s?      optional plural
    \\s*        optional spaces                   [\\s-]?  optional space or hyphen
"""

INTENTS = [
    # ------------------------------------------------------------------ B05
    {
        "id": "B05",
        "name": "Lost Baggage",
        "patterns": [
            # "lost my bag", "missing checked baggage", "damaged suitcase"
            # (at most one word between, so "lost my pass in my bag" is NOT matched)
            r"\b(?:lost|missing|misplaced|damaged|broken|torn|stolen)\s+(?:(?:my|the|a|our)\s+)?(?:\w+\s+)?(?:luggage|baggage|bags?|suitcases?)\b",
            # "my suitcase did not arrive", "luggage never came", "bag is damaged"
            r"\b(?:luggage|baggage|bags?|suitcases?)\b.{0,25}\b(?:lost|missing|misplaced|damaged|broken|torn|stolen|not arrive|not come|never (?:arrived|came)|did(?:n't| not) (?:arrive|come|show up))\b",
            # "can't find my bag"
            r"\bcan(?:'|no)?t find my (?:luggage|baggage|bags?|suitcases?)\b",
        ],
        "response": (
            "If your luggage is missing or damaged, immediately visit your "
            "airline's baggage service desk at the airport before leaving the "
            "arrival area. Report the bag and request a Property Irregularity "
            "Report (PIR) or reference number. Keep your boarding pass and "
            "baggage tag receipt safely. Provide your contact details and "
            "baggage description, and follow up with the airline using your "
            "reference number. You may also be eligible for compensation "
            "depending on the airline's policy."
        ),
    },
    # ------------------------------------------------------------------ B04
    {
        "id": "B04",
        "name": "Liquid Restrictions",
        "patterns": [
            # any mention of liquids, gels, aerosols or 100 ml
            r"\b(?:liquids?|gels?(?!\s+pens?)|aerosols?|100\s*ml)\b",
            # "can I bring water in my bag", "is perfume allowed"
            r"\b(?:water|perfume|shampoo|juice|bottles?)\b.{0,25}\b(?:carry|bring|take|allowed|cabin|hand|flight)\b",
            r"\b(?:carry|bring|take)\b.{0,25}\b(?:water|perfume|shampoo|juice|bottles?)\b",
        ],
        "response": (
            "Generally, liquids, gels and aerosols in cabin baggage must be "
            "stored in individual containers of no more than 100 ml each. "
            "They should usually fit inside one transparent, resealable "
            "1-litre plastic bag. Exceptions may apply to medicines and "
            "baby food. Rules can vary by airport and country, so please "
            "confirm the requirements with your airline or airport."
        ),
    },
    # ------------------------------------------------------------------ B03
    {
        "id": "B03",
        "name": "Laptop and Electronics",
        "patterns": [
            # laptops: "laptop", "macbook"
            r"\b(?:laptops?|macbooks?|ipads?)\b",
            # other electronics: "power bank", "powerbank", "camera", "charger"
            r"\bpower[\s-]?banks?\b",
            # camera/charger/gadget only count when a carrying word is nearby
            r"\b(?:cameras?|chargers?|electronics?|gadgets?)\b.{0,25}\b(?:carry|bring|take|pack|allowed|cabin|hand|baggage|luggage|flight)\b",
            r"\b(?:carry|bring|take|pack)\b.{0,25}\b(?:cameras?|chargers?|electronics?|gadgets?)\b",
        ],
        "response": (
            "Yes, you can generally carry a laptop and other electronics in "
            "your cabin baggage. It is recommended to keep them in your hand "
            "luggage rather than checked baggage. Power banks and spare "
            "lithium batteries are usually allowed only in cabin baggage, not "
            "in checked baggage. You may be asked to remove electronics "
            "separately during security screening. Please confirm any "
            "specific requirements with your airline and airport."
        ),
    },
    # ------------------------------------------------------------------ B01
    {
        "id": "B01",
        "name": "Cabin Baggage Allowance",
        "patterns": [
            # "cabin bag", "hand luggage", "carry-on baggage"
            r"\b(?:cabin|hand|carry[\s-]?on|onboard)\s+(?:baggage|luggage|bags?)\b",
            # "how many bags in the cabin", "how many bags can I carry on"
            r"\bhow\s+(?:many|much)\b.{0,25}\b(?:bags?|baggage|luggage)\b.{0,25}\b(?:cabin|carry[\s-]?on|on board)\b",
            # "carry-on size", "carry on limit" (but not "carry on with my trip")
            r"\bcarry[\s-]?on\s+(?:size|limit|allowance|weight|rules?)\b",
        ],
        "response": (
            "Most airlines allow one cabin bag, usually weighing around 7 kg. "
            "The permitted dimensions and weight may vary depending on the "
            "airline and ticket class. Please confirm the exact allowance "
            "with your airline before travelling."
        ),
    },
    # ------------------------------------------------------------------ B02
    {
        "id": "B02",
        "name": "Check-in Baggage Allowance",
        "patterns": [
            # "checked bag", "check-in luggage", "hold baggage"
            r"\b(?:check[\s-]?in|checked|hold)\s+(?:baggage|luggage|bags?)\b",
            # "luggage I can check in", "baggage to be checked"
            r"\b(?:baggage|luggage|bags?|suitcases?)\b.{0,25}\bcheck(?:ed)?[\s-]?in\b",
            # general questions: "baggage allowance", "how much baggage can I carry"
            r"\b(?:baggage|luggage)\s+(?:allowance|limit)\b",
            r"\bhow\s+(?:much|many)\b.{0,25}\b(?:baggage|luggage|bags?|suitcases?)\b.{0,25}\b(?:carry|take|bring|allowed)\b",
            # "how many kg can I take", "kilos allowed"
            r"\b(?:kgs?|kilos?|kilograms?)\b.{0,25}\b(?:allowed|limit|carry|take|bring)\b",
            r"\bhow\s+many\s+(?:kgs?|kilos?|kilograms?)\b",
            # excess baggage: "excess baggage fee", "my bag is overweight"
            r"\b(?:excess|extra|overweight|over[\s-]?weight)\s+(?:baggage|luggage|bags?|weight|fees?|charges?)\b",
            r"\b(?:baggage|luggage|bags?|suitcases?)\b.{0,20}\b(?:overweight|over[\s-]?weight|too heavy|over the limit)\b",
        ],
        "response": (
            "Check-in baggage allowance depends on your airline, ticket class "
            "and destination. Many domestic economy flights allow approximately "
            "15 kg of checked baggage. International allowances may differ. "
            "Baggage above the allowance is usually charged as excess baggage, "
            "so check the fee with your airline before travelling. "
            "Please confirm your exact baggage allowance with your airline."
        ),
    },
]
