## Scanner State Transition

In my implementation there are following tokens present:

- WS - whitespace, tabs, newline char (ignored)
- SYMBOL - special meaning character: SYMBOLS := \[ "<", "/>", ">", "/>", "=" \]
- TEXT - free text that is just floating around, can be composed by alpha characters or "_"
- STRING - text composed by ANY character, except: STR_BREAK := \[ "\n", EOF \]. This string of characters MUST be wrapped by quotes

We shall implement this as a state machine to prevent any accidental errors due to forgotten state transitions or other
mistakes.

START_STATE:

- on WS: GOTO START STATE 
- on alpha: GOTO TEXT_INPUT

TEXT_INPUT:

- on alpha or "_": GOTO TEXT_INPUT (and append the char)
- on WS: GOTO START_STATE (and yield currently accumulated text)
- on "<": GOTO SYMBOL (and yield currently accumulated text)
- on ">": GOTO SYMBOL (and yield currently accumulated text)
- on "/": error: this is impossible!
- on numeric char: error: this is impossible!

SYMBOL_INPUT:

- on any char in FLAT_UNIQUE(SYMBOLS): append to accumulated text.
  if accumulated SYMBOL is not in the SYMBOLS list: error. else: GOTO SYMBOL
- on alpha: GOTO TEXT_INPUT (and yield current SYMBOL)
- on QUOTE: GOTO STRING_INPUT (and yield current SYMBOL)
- else: invalid transition

STRING_INPUT:

- on any char except one in STR_BREAK: append to accumulated text
- on QUOTE: GOTO STRING_END

STRING_END:

- on WS: yield curren STRING and GOTO START_STATE
- else: error: QUOTE cannot be followed by non WS character

Note: FLAT_UNIQUE is a special function that take in a list of strings, and
returns all unique characters across all strings combined
