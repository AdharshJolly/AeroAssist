"""main.py - the program you run. It is the command-line chat screen.

WHAT THIS FILE DOES
  * Starts AeroAssist: prints the welcome banner, then repeatedly asks
    "You:", sends your text to the chat engine and prints the answers.
  * Contains NO regex and NO airport knowledge. It only does input/output.
  * If any member module is broken (bad regex, missing field...) the engine
    raises a RegistryError; this file prints it clearly and stops with exit
    code 1 instead of hiding the problem.
  * Leaves cleanly on "exit", Ctrl+C or end of input, and survives an error
    on a single question without crashing the whole chat.

HOW TO USE
  python main.py            normal chat
  python main.py --debug    also shows the matched intent id, module name
                            and the values extracted by named groups

MAIN PIECES
  banner()    builds the welcome text
  show_reply  prints one answer (wrapped to fit the terminal)
  run_chat    the input loop
  main        reads --debug, builds the ChatEngine, starts run_chat
"""

import argparse
import sys
import traceback

from chatbot import config
from chatbot.engine import ChatEngine
from chatbot.registry import RegistryError
from chatbot.response_handler import wrap_text

LINE = "=" * config.BANNER_WIDTH


def banner():
    return "\n".join([
        LINE,
        config.APP_NAME.upper().center(config.BANNER_WIDTH),
        config.TAGLINE.upper().center(config.BANNER_WIDTH),
        LINE,
        "",
        f"Welcome to {config.APP_NAME}!",
        "",
        "I can help you with:",
        "",
        "1. Flight Information",
        "2. Check-in & Boarding",
        "3. Baggage Assistance",
        "4. Security & Airport Facilities",
        "",
        "Type 'help' to see available topics.",
        "Type 'exit' to end the conversation.",
        "",
        LINE,
    ])


def show_reply(reply, write, debug):
    write("\nAeroAssist:")
    write(wrap_text(reply.text))
    if debug:
        if reply.kind == "intent":
            write(f"[DEBUG] intent={reply.intent_id} ({reply.intent_name}) | "
                  f"module={reply.module} | groups={reply.groups}")
        else:
            write(f"[DEBUG] kind={reply.kind} | query={reply.query!r}")


def run_chat(engine, read=input, write=print, debug=False):
    """The conversation loop."""
    write(banner())
    while True:
        try:
            user_text = read("\nYou: ")
        except (EOFError, KeyboardInterrupt):
            write("\n\nAeroAssist:\n" + config.GOODBYE_RESPONSE)
            return
        try:
            replies = engine.respond(user_text)
        except Exception:  # keep the chat alive, but never hide the error in debug mode
            write("\nAeroAssist:\n" + config.ERROR_RESPONSE)
            if debug:
                write(traceback.format_exc())
            continue
        for reply in replies:
            show_reply(reply, write, debug)
        if any(reply.kind == "exit" for reply in replies):
            return


def main(argv=None):
    parser = argparse.ArgumentParser(description="AeroAssist airport assistance chatbot")
    parser.add_argument("--debug", action="store_true", help="show matched intent id and module")
    args = parser.parse_args(argv)

    try:
        engine = ChatEngine()
    except RegistryError as error:
        print("AeroAssist cannot start because a member module is invalid:\n", file=sys.stderr)
        print(error, file=sys.stderr)
        return 1

    run_chat(engine, debug=args.debug)
    return 0


if __name__ == "__main__":
    sys.exit(main())
