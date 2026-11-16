"""registry.py - loads, checks and compiles every member's intents.

WHAT THIS FILE DOES
  * Imports the INTENTS list from each member module (MEMBER_SOURCES lists
    them in priority order: Member 1 first, then 2, 3, 4).
  * Validates every ACTIVE intent and compiles its regex patterns with
    re.IGNORECASE. It checks: required fields (id, name, patterns, response),
    unique ids, valid regex, non-empty response and pattern list, patterns
    that would match empty text (too broad), and that every {placeholder} in
    the response has a matching (?P<name>...) group (or a default, or a lookup).
  * Skips intents marked "active": False (placeholders).
  * Collects ALL problems into one RegistryError that names the member, the
    intent id and the pattern, so nothing fails silently.
  * Returns a list of Intent objects for the engine.

HOW MEMBERS INTERACT
  Members never edit this file. Adding a member module = one import line and
  one line in MEMBER_SOURCES.

OPTIONAL "lookups" KEY
  An intent may define {"airline": {"from": "airline_code", "table": {...}}}.
  The engine then fills {airline} from a static table (see Member 1).
"""

import re
from dataclasses import dataclass, field

from chatbot.response_handler import required_placeholders
from members.member_1.flight_information import INTENTS as MEMBER_1_INTENTS
from members.member_2.checkin_boarding import INTENTS as MEMBER_2_INTENTS
from members.member_3.baggage_assistance import INTENTS as MEMBER_3_INTENTS
from members.member_4.security_facilities import INTENTS as MEMBER_4_INTENTS

# (member number, module title, that member's INTENTS list)
# The ORDER here is the matching priority between members (see README).
MEMBER_SOURCES = [
    (1, "Flight Information", MEMBER_1_INTENTS),
    (2, "Check-in & Boarding", MEMBER_2_INTENTS),
    (3, "Baggage Assistance", MEMBER_3_INTENTS),
    (4, "Security & Airport Facilities", MEMBER_4_INTENTS),
]

REQUIRED_FIELDS = ("id", "name", "patterns", "response")


class RegistryError(Exception):
    """Raised when one or more member intents are invalid."""


@dataclass
class Intent:
    """A validated intent with its patterns already compiled."""

    id: str
    name: str
    member: int
    module: str
    patterns: list = field(default_factory=list)  # compiled re.Pattern objects
    response: str = ""
    lookups: dict = field(default_factory=dict)  # optional static tables (see response_handler)


def _check_intent(raw, where, label):
    """Validate one ACTIVE intent. Returns (list of problems, compiled patterns)."""
    problems = []
    compiled = []

    for key in REQUIRED_FIELDS:
        if key not in raw:
            problems.append(f"{label}: missing required field '{key}'")
    if problems:
        return problems, compiled

    if not isinstance(raw["name"], str) or not raw["name"].strip():
        problems.append(f"{label}: 'name' must be a non-empty string")

    response = raw["response"]
    if not isinstance(response, str) or not response.strip():
        problems.append(f"{label}: 'response' must be a non-empty string")
        response = ""

    lookups = raw.get("lookups", {})
    if not isinstance(lookups, dict):
        problems.append(f"{label}: 'lookups' must be a dictionary")
        lookups = {}
    for lookup_name, spec in lookups.items():
        if not (isinstance(spec, dict) and isinstance(spec.get("from"), str)
                and isinstance(spec.get("table"), dict)):
            problems.append(f"{label}: lookup '{lookup_name}' needs {{'from': group_name, 'table': {{...}}}}")
            lookups = {}
            break

    patterns = raw["patterns"]
    if not isinstance(patterns, list) or not patterns:
        problems.append(f"{label}: 'patterns' must be a non-empty list")
        return problems, compiled

    for pattern in patterns:
        if not isinstance(pattern, str):
            problems.append(f"{label}: pattern {pattern!r} is not a string")
            continue
        try:
            regex = re.compile(pattern, re.IGNORECASE)
        except re.error as error:
            problems.append(f"{label}: invalid regex {pattern!r} -> {error}")
            continue
        if regex.search(""):
            problems.append(f"{label}: pattern {pattern!r} matches empty text (too broad)")
            continue
        for name in required_placeholders(response, provided=lookups):
            if name not in regex.groupindex:
                problems.append(
                    f"{label}: response uses {{{name}}} but pattern {pattern!r} has no "
                    f"named group (?P<{name}>...). Add the group or use {{{name}|default}}."
                )
        compiled.append(regex)
    # A lookup may read an OPTIONAL group, but at least one pattern must define it
    # (otherwise it is probably a typo and could never work).
    for lookup_name, spec in lookups.items():
        if compiled and not any(spec["from"] in regex.groupindex for regex in compiled):
            problems.append(
                f"{label}: lookup '{lookup_name}' reads group '{spec['from']}' "
                f"but no pattern defines (?P<{spec['from']}>...)"
            )
    return problems, compiled


def build_registry(sources=None):
    """Validate all members and return a list of Intent objects, in priority order.

    `sources` defaults to MEMBER_SOURCES.
    """
    sources = MEMBER_SOURCES if sources is None else sources
    problems = []
    seen_ids = {}
    registry = []

    for member, title, intents in sources:
        where = f"Member {member} ({title})"
        if not isinstance(intents, list):
            problems.append(f"{where}: INTENTS must be a list")
            continue

        for position, raw in enumerate(intents, start=1):
            if not isinstance(raw, dict):
                problems.append(f"{where}: intent #{position} must be a dictionary")
                continue
            intent_id = raw.get("id")
            if not isinstance(intent_id, str) or not intent_id.strip():
                problems.append(f"{where}: intent #{position} has no valid 'id'")
                continue
            label = f"{where}, intent {intent_id}"

            if intent_id in seen_ids:
                problems.append(f"{label}: duplicate id (already used by {seen_ids[intent_id]})")
            else:
                seen_ids[intent_id] = where

            if raw.get("active", True) is False:
                continue  # placeholder: skipped on purpose

            intent_problems, compiled = _check_intent(raw, where, label)
            problems.extend(intent_problems)
            if not intent_problems:
                registry.append(Intent(intent_id, raw["name"], member, title, compiled,
                                       raw["response"], raw.get("lookups", {})))

    if problems:
        raise RegistryError(
            "Found %d problem(s) in the member modules:\n  - %s" % (len(problems), "\n  - ".join(problems))
        )
    return registry
