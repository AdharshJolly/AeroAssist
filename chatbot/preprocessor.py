"""preprocessor.py - cleans the user's message and splits it into questions.

WHAT THIS FILE DOES
  preprocess(text) turns one raw message into a list of clean "segments"
  (one per question), so the engine can answer each separately.

  Steps, in order:
    1. re.sub  - collapse repeated punctuation ("???" -> "?"), using a
                 capturing group and a back-reference.
    2. re.split - cut the text at ";", at new lines, and right after a "?"
                 (a look-behind), so "A? B?" becomes two questions.
    3. re.sub  - squeeze extra spaces, remove spaces before punctuation and
                 strip leading punctuation.
    4. Drop segments with no letters/digits (nothing to answer).

  It never lower-cases the text: flight numbers keep their shape and the
  matching itself is case-insensitive (re.IGNORECASE).
"""

import re


def preprocess(text):
    """Return a list of clean query segments found in `text`.

    Example:
        >>> preprocess("  What is a boarding pass??   ; Can I carry a laptop?  ")
        ['What is a boarding pass?', 'Can I carry a laptop?']

    Flight numbers such as AI2025 or 6E123 are never touched: we only split on
    '?', ';' and line breaks, and we never delete letters or digits.
    Empty or whitespace-only input returns an empty list.
    """
    if not text or not text.strip():
        return []

    # re.sub #1: collapse repeated punctuation ("???" -> "?", ";;" -> ";").
    # (\1) is a back-reference to the character captured by ([?!.,;]).
    text = re.sub(r"([?!.,;])\1+", r"\1", text)

    # re.split: cut at semicolons / line breaks, or right AFTER a question mark.
    # (?<=\?) is a "look-behind": it matches the empty spot after a '?', so
    # the '?' stays attached to its own question.
    parts = re.split(r"[;\n\r]+|(?<=\?)", text)

    segments = []
    for part in parts:
        part = re.sub(r"\s+", " ", part).strip()          # re.sub #2: tidy spaces
        part = re.sub(r"\s+([?!.,])", r"\1", part)        # re.sub #3: "flight ?" -> "flight?"
        part = re.sub(r"^[?!.,\s]+", "", part)            # re.sub #4: drop stray leading punctuation
        if re.search(r"\w", part):                        # keep only segments with real content
            segments.append(part)
    return segments
