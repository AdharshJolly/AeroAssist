"""chatbot package - the core of AeroAssist (shared by all members).

Members never edit these files. Overview:
  config.py            fixed texts, banner settings, greeting/help/exit patterns
  preprocessor.py      cleans input and splits it into separate questions
  registry.py          loads and validates every member's INTENTS
  engine.py            finds the matching intent and builds the reply
  response_handler.py  fills {placeholders}, wraps text, builds the help text
"""
