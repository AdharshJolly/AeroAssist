
"""
security_facilities.py - Member 4: Security & Airport Facilities (S01-S05)

Handles:
S01 - Domestic Travel Documents
S02 - Security Screening
S03 - Power Bank Transportation
S04 - Wheelchair Assistance
S05 - Lost and Found
"""

INTENTS = [

    # S01 - Domestic Travel Documents
    {
        "id": "S01",
        "name": "Domestic Travel Documents",
        "patterns": [
            r"\bwhat (?:documents|ids|identification) (?:do i need|are required) for (?:a )?domestic flight\b",
            r"\b(?:documents|id proof|identity proof) required for domestic travel\b",
            r"\bwhat should i carry for a domestic flight\b",
            r"\bcan i travel domestically with (?P<document>aadhar|aadhaar|pan card|passport|driving license|voter id)\b",
            r"\b(?:is|will) (?P<document>aadhar|aadhaar|pan card|passport|driving license|voter id) accepted for domestic flights\b",
        ],
        "response": (
            "For domestic flights within India, you generally need a valid flight "
            "ticket or booking confirmation and an accepted photo identity document. "
            "Commonly accepted IDs include Aadhaar, m-Aadhaar, passport, voter ID, "
            "PAN card, driving licence and eligible government-issued photo IDs. "
            "Eligible DigiLocker-issued documents are also accepted. "
            "Ensure that your name matches your flight booking. "
            "Requirements for children and other special cases may differ. "
            "Please confirm the accepted documents with your airline before travelling."
        ),
    },

    # S02 - Security Screening
    {
        "id": "S02",
        "name": "Security Screening",
        "patterns": [
            r"\bwhat happens during airport security (?:check|screening)\b",
            r"\bwhat items are prohibited (?:at|during) airport security\b",
            r"\bcan i carry (?P<item>knives|scissors|liquids|sharp objects|tools|flammable items) through airport security\b",
            r"\b(?:is|are) (?P<item>knives|scissors|liquids|sharp objects|tools|flammable items) allowed in (?:hand|cabin) baggage\b",
            r"\bwhat should i remove (?:from my bag|before security screening)\b",
            r"\bairport security checking procedure\b",
        ],
        "response": (
            "Airport security screening is conducted to ensure passenger and "
            "flight safety. You and your cabin baggage will be screened before "
            "boarding. Follow instructions from security personnel and keep your "
            "boarding pass and identification ready. Sharp objects such as knives, "
            "certain scissors, weapons and flammable materials are restricted or "
            "prohibited in cabin baggage. Some items may be permitted in checked "
            "baggage subject to airline rules. If you are unsure about a particular "
            "item, check your airline's restricted-items list before packing."
        ),
    },

    # S03 - Power Bank Transportation
    {
        "id": "S03",
        "name": "Power Bank Transportation",
        "patterns": [
            r"\bcan i carry (?:a )?power bank (?:on|in) (?:a )?(?:flight|plane|aircraft)\b",
            r"\bare power banks allowed (?:on flights|in airplanes|in hand baggage)\b",
            r"\bcan i put (?:my )?power bank in (?:my )?checked baggage\b",
            r"\b(?:what is the|is there a) power bank (?:capacity )?limit\b",
            r"\b(?:is )?(?P<capacity>\d+\s*(?:mah|mAh|wh|Wh)) power bank allowed\b",
            r"\bpower bank (?:flight|airline) rules\b",
            # any other power bank question
            r"\bpower[\s-]?banks?\b",
        ],
        "response": (
            "Power banks must generally be carried in cabin/hand baggage and "
            "not in checked baggage. Under common airline rules, power banks "
            "up to 100 Wh are permitted, subject to airline approval and "
            "applicable restrictions. Protect the terminals against short circuits. "
            "Do not use or charge the power bank onboard where prohibited by "
            "your airline. Some airlines also restrict the number of power banks "
            "and their storage location. Please confirm the latest rules with "
            "your airline before departure."
        ),
    },

    # S04 - Wheelchair Assistance
    {
        "id": "S04",
        "name": "Wheelchair Assistance",
        "patterns": [
            r"\bhow can i (?:request|book|arrange) wheelchair assistance\b",
            r"\bdo airports provide wheelchairs for passengers\b",
            r"\bi need (?P<assistance>wheelchair|mobility) assistance at the airport\b",
            r"\bhow do i get a wheelchair at the airport\b",
            r"\bcan i request special assistance for a disabled passenger\b",
            r"\bwheelchair assistance (?:booking|service|request)\b",
        ],
        "response": (
            "Airlines and airports generally provide wheelchair assistance "
            "for passengers with reduced mobility. Contact your airline when "
            "booking your ticket or at least 48 hours before departure, if possible. "
            "You can also inform the airline staff at the airport check-in counter. "
            "Mention whether you need assistance from the terminal entrance, "
            "through security, to the aircraft, or during arrival. If you use "
            "a battery-powered wheelchair, inform your airline about its battery "
            "type and specifications in advance. Please confirm the arrangements "
            "directly with your airline."
        ),
    },

    # S05 - Lost and Found
    {
        "id": "S05",
        "name": "Lost and Found",
        "patterns": [
            r"\bi (?:have )?lost (?:my )?(?P<item>bag|baggage|luggage|phone|mobile|wallet|passport|handbag|laptop) (?:at|in) (?:the )?airport\b",
            r"\bwhere is (?:the )?(?:airport )?lost and found\b",
            r"\bhow can i report (?:a )?lost (?P<item>item|bag|phone|wallet|luggage)\b",
            r"\bi cannot find (?:my )?(?P<item>bag|luggage|phone|wallet|passport|handbag)\b",
            r"\bwhat should i do if i lose something at the airport\b",
            r"\b(?:lost|missing) (?:my )?(?P<item>belongings|baggage|luggage|personal item)\b",
            # "is there a lost and found", "lost & found office"
            r"\blost\s*(?:and|&)\s*found\b",
        ],
        "response": (
            "If you have lost an item at the airport, contact the airport's "
            "Lost and Found office or information desk as soon as possible. "
            "Provide a description of the item, the approximate time and the "
            "location where you last saw it. Keep your boarding pass and baggage "
            "tag available if applicable. If your checked baggage is missing, "
            "report it immediately to your airline's baggage services desk "
            "before leaving the airport. AeroAssist cannot access live lost-item "
            "records, so please contact the relevant airport or airline directly."
        ),
    },

]
