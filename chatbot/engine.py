"""engine.py - the brain: turns what the user typed into replies.

WHAT THIS FILE DOES
  respond(text) -> list of Reply objects (one per question in the message):
    1. preprocess() cleans and splits the message.
    2. For each question, commands are checked first with re.match():
       exit, help, greeting.
    3. Otherwise every intent's patterns are tried with re.search(), in a
       fixed order, and the FIRST match wins:
         Member 1 -> 4, then the order of each member's INTENTS list,
         then the order of each intent's patterns.
    4. The named groups of the match (e.g. flight_code) are extracted,
       cleaned and inserted
       into the response template.
    5. No match -> the fixed default response.

  The engine contains NO airport patterns; they all live in the member
  modules. Reply carries the text plus debug info (intent id, module, groups).
"""

import re
from dataclasses import dataclass, field

from chatbot import config
from chatbot.preprocessor import preprocess
from chatbot.registry import MEMBER_SOURCES, build_registry
from chatbot.response_handler import build_help, clean_groups, fill_template

# Compiled once. re.match() is used because commands must START the text.
GREETING_RE = re.compile(config.GREETING_PATTERN, re.IGNORECASE)
EXIT_RE = re.compile(config.EXIT_PATTERN, re.IGNORECASE)
HELP_RE = re.compile(config.HELP_PATTERN, re.IGNORECASE)


@dataclass
class Reply:
    """One answer. kind is: intent, default, greeting, help, exit or empty."""

    kind: str
    text: str
    query: str = ""
    intent_id: str = ""
    intent_name: str = ""
    module: str = ""
    groups: dict = field(default_factory=dict)


class ChatEngine:
    def __init__(self, intents=None):
        """`intents` defaults to every validated intent from the registry."""
        self.intents = build_registry() if intents is None else intents

    # -- command handling (re.match) ---------------------------------------
    def _command_reply(self, query):
        """Return a Reply for greeting/help/exit commands, else None."""
        if EXIT_RE.match(query):
            return Reply("exit", config.GOODBYE_RESPONSE, query)
        if HELP_RE.match(query):
            return Reply("help", self.help_text(), query)
        if GREETING_RE.match(query):
            return Reply("greeting", config.GREETING_RESPONSE, query)
        return None

    def help_text(self):
        topics = []
        for _, title, _ in MEMBER_SOURCES:
            names = list(dict.fromkeys(i.name for i in self.intents if i.module == title))
            topics.append((title, names))
        return build_help(topics)

    # -- intent matching (re.search) ---------------------------------------
    def find_intent(self, query):
        """Return (intent, match) for the first matching pattern, or None."""
        for intent in self.intents:
            for pattern in intent.patterns:
                match = pattern.search(query)
                if match:
                    return intent, match
        return None

    def answer(self, query):
        """Answer ONE query segment."""
        command = self._command_reply(query)
        if command:
            return command

        found = self.find_intent(query)
        if not found:
            return Reply("default", config.DEFAULT_RESPONSE, query)

        intent, match = found
        groups = clean_groups(match.groupdict())
        text = fill_template(intent.response, groups)
        return Reply("intent", text, query, intent.id, intent.name, intent.module, groups)

    # -- whole user message -------------------------------------------------
    def respond(self, text):
        """Answer a full user message (may hold several questions)."""
        segments = preprocess(text)
        if not segments:
            return [Reply("empty", config.EMPTY_INPUT_RESPONSE)]
        return [self.answer(segment) for segment in segments]
