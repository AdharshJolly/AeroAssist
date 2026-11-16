"""config.py - central settings and fixed messages for AeroAssist.

WHAT THIS FILE DOES
  Holds everything that does not belong to one specific member:
    * branding (APP_NAME, TAGLINE) and display widths for the banner/replies
    * the fixed replies: default ("I'm sorry, I couldn't understand..."),
      empty input, greeting, goodbye and internal-error messages
    * the regex patterns for the three chat commands - greeting, help and
      exit. They are used with re.match() (the command must be at the START
      of the text) and end with $ so "exit the terminal" is not an exit.
    * UPPERCASE_GROUP_SUFFIXES: named groups ending in "_code" are shown in
      upper case (ai2025 -> AI2025).

WHEN TO EDIT
  Only to change wording or the command patterns. Question patterns for
  airport topics belong in the member modules, not here.
"""

APP_NAME = "AeroAssist"
TAGLINE = "Your Virtual Airport Assistance Desk"
BANNER_WIDTH = 50
WRAP_WIDTH = 70  # line width used when printing replies

# ---------------------------------------------------------------------------
# Fixed messages
# ---------------------------------------------------------------------------
DEFAULT_RESPONSE = (
    "I'm sorry, I couldn't understand your query. You can ask me about "
    "flight information, check-in, baggage, security procedures or airport "
    "facilities."
)
EMPTY_INPUT_RESPONSE = "Please type a question, or type 'help' to see what I can answer."
GREETING_RESPONSE = (
    "Hello! I'm AeroAssist, your virtual airport assistance desk. "
    "Ask me a question, or type 'help' to see the topics I cover."
)
GOODBYE_RESPONSE = "Thank you for using AeroAssist. Have a safe and pleasant journey!"
ERROR_RESPONSE = "Sorry, something went wrong while handling that question. Please try again."

# ---------------------------------------------------------------------------
# Chat-command patterns.  They are used with re.match(), which only looks at
# the START of the text, so each pattern ends with `$` to demand a full match.
# ---------------------------------------------------------------------------
GREETING_PATTERN = r"\s*(?:hi|hello|hey|namaste|good\s+(?:morning|afternoon|evening))(?:\s+there)?\b[\s,!.?]*$"
EXIT_PATTERN = r"\s*(?:exit|quit|bye|goodbye)\b[\s!.?]*$"
HELP_PATTERN = r"\s*(?:help|topics|menu)\b[\s!.?]*$"

# Group names ending with one of these suffixes are upper-cased before they
# are put into a response (so "6e123" is shown as "6E123").
UPPERCASE_GROUP_SUFFIXES = ("_code",)
