"""response_handler.py - builds the text that is shown to the user.

WHAT THIS FILE DOES
  Response templates written by members can contain placeholders:
      {flight_code}              replaced by the value of the named group
      {flight_code|your flight}  same, but uses the text after | when the
                                 group did not match (optional information)
  A missing value never crashes the chatbot.

  Functions:
    required_placeholders  names a pattern MUST capture (used by the registry)
    clean_groups           drops unmatched groups, trims, upper-cases *_code
    apply_lookups          adds values from a member's static table
                           (airline_code "6E" -> airline "IndiGo")
    fill_template          re.sub() with a function that does the replacing
    wrap_text              wraps long lines for the terminal, keeps line breaks
    build_help             builds the help screen from the loaded intents
"""

import re
import textwrap

from chatbot import config

# {name} or {name|default text}
PLACEHOLDER_RE = re.compile(r"\{(?P<name>\w+)(?:\|(?P<default>[^{}]*))?\}")


def required_placeholders(template, provided=()):
    """Names used in `template` that have NO default (so the pattern must capture them).

    `provided` = names filled another way (the intent's "lookups"), so they are not required.
    """
    return [m["name"] for m in PLACEHOLDER_RE.finditer(template)
            if m["default"] is None and m["name"] not in provided]


def clean_groups(groupdict):
    """Drop unmatched (None) groups, strip spaces, upper-case `*_code` values."""
    cleaned = {}
    for name, value in groupdict.items():
        if value is None or not value.strip():
            continue
        value = value.strip()
        if name.endswith(config.UPPERCASE_GROUP_SUFFIXES):
            value = value.upper()
        cleaned[name] = value
    return cleaned


def apply_lookups(groups, lookups):
    """Add values found in a member's static table, e.g. airline_code 'AI' -> airline 'Air India'.

    `lookups` = {"airline": {"from": "airline_code", "table": {"AI": "Air India", ...}}}
    If the key is missing or not in the table, nothing is added (the template default is used).
    """
    enriched = dict(groups)
    for name, spec in (lookups or {}).items():
        value = spec["table"].get(groups.get(spec["from"], ""))
        if value:
            enriched[name] = value
    return enriched


def fill_template(template, groups):
    """Insert extracted values into a response template using re.sub()."""

    def replace(match):
        # value if we captured one, else the default text, else nothing
        return groups.get(match["name"]) or match["default"] or ""

    return PLACEHOLDER_RE.sub(replace, template)


def wrap_text(text, width=config.WRAP_WIDTH):
    """Wrap long lines for the terminal while keeping existing line breaks."""
    lines = text.split("\n")
    return "\n".join(textwrap.fill(line, width) if line.strip() else "" for line in lines)


def build_help(module_topics):
    """Help text. `module_topics` is a list of (module title, [intent names])."""
    lines = ["I can help you with these topics:", ""]
    for number, (title, names) in enumerate(module_topics, start=1):
        lines.append(f"{number}. {title}")
        if names:
            lines.extend(f"     - {name}" for name in names)
        else:
            lines.append("     (coming soon)")
    lines += ["", "Type a question in your own words, e.g. 'What is the status of flight AI2025?'",
              "You can ask several questions at once by separating them with ';' or '?'.",
              "Type 'exit' to end the conversation."]
    return "\n".join(lines)
