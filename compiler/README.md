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


## Parser State Transition

Now that we have our TOKENS defined, it is time to define the transitions on those tokens.
In my mind, it is way easier to first strongly define our grammar using the regular expressions.
We will start by defining ATTRIBUTE pattern:

- `ATTRIBUTE` := TEXT(*) SYMBOL(=) STRING(*)

and now, we can use it to define ELEMENT pattern. But there is more than one! So we will start with a basics:

- `ELEMENT_START` := SYMBOL(<) TEXT(*) ATTRIBUTE* SYMBOL(>)
- `ELEMENT_END` := SYMBOL(<) TEXT(*) SYMBOL(>)

and now, let us define the ELEMENT:

- ELEMENT := ELEMENT_START ELEMENT* ELEMENT_END      # This will be parsed in Semantic Analysis (later) stage!
- ELEMENT := SYMBOL(<) TEXT(*) ATTRIBUTE* SYMBOL(/>) # This is SelfClosingToken

Let us now define some states:

START_STATE:

- on SYMBOL(<): GOTO ELEMENT_START (initialize with the StartToken(name=None, accumulated=None)
- else: raise error. our xml HAS TO START with the `<root>` tag

IN_DOCUMENT:

- on SYMBOL(<): GOTO ELEMENT_START (initialize with the StartToken(name=None, accumulated=None)
- on SYMBOL(</): GOTO ELEMENT_END 
- else: raise error. our xml HAS TO START with the `<root>` tag

ELEMENT_START:

- on TEXT: set StartToken name to TEXT.value, GOTO: ELEMENT_ATTR_SET
- else: raise error. There HAS TO BE name to the xml tag

ELEMENT_ATTR_SET:

- on TEXT: Create new ElementAttribute instance with TEXT.value and empty
  string, then create new list of StartToken attributes.
  Finally: GOTO ATTRIBUTE_SET
- on SYMBOL(/>): yield current XmlToken as SelfClosingToken with the same name
  as current StartToken and attributes
- on SYMBOL(>): yield current StartToken, GOTO IN_DOCUMENT

ATTRIBUTE_SET:

- on SYMBOL(=): GOTO ATTRIBUTE_SET_VALUE
- else: raise error: there can be no other pattern than `ATTRIBUTE` from earlier sections

ATTRIBUTE_SET_VALUE:

- on STRING(*): Create new value from the last value in the list of attributes
  and create new list with value of the attribute set to STRING.value (Notice
  that our dataclass is frozen!). Finally, GOTO ELEMENT_START
- else: raise error: there can be no other pattern than `ATTRIBUTE` from earlier sections

ELEMENT_END:

- on TEXT: set name to TEXT.value, GOTO ELEMENT_END_VERIFY
- else: raise error. There has to be a name to the closing element

ELEMENT_END_VERIFY:

- on SYMBOL(>): yield current EndToken, GOTO IN_DOCUMENT
- else: raise error. There can be no other structure in closing element than 

## Semantic Analysis

From the previous step we have an Iterable of XmlTokens.
Now, it makes sense to both:

- Analyze if all tokens follow the basic rules
- Create a Typed AST, that is easy to parse recursively

First, let us define what we will expect on the output. Basic tree like:

```xml 
<root>
    <kitten Name="Whiskers">
        <parent>
            <cat Name="The Garfield"/>
        </parent>
    </kitten>
</root>
```

Should become (skiping scanner + parser stages):

```json
{
    "element_name": "root",
    "children": [
        {
            "element_name": "kitten",
            "attributes": [
                {
                    "name": "Name",
                    "value": "Whiskers"
                },
            ],
            "children": [
                {
                    "element_name": "parent",
                    "attributes": null,
                    "children": [
                        {
                            "element_name": "cat",
                            "attributes": [
                                {
                                    "name": "Name",
                                    "value": "The Garfield"
                                },
                            ],
                            "children": null
                        }
                    ]
                }
            ]
        }
    ]
}
```

This way, we will get easy to parse XmlElements.

### Verify the correctness

From the nature of the Tokens (Start/End) this is actually a classical CS
problem. This example is usually in the form: "Having symbols `()[]{}` make
sure the input string has valid order of symbols"; Examples:

- Correct: `()[]{}`, `{(())[]}`, etc.
- InCorrect: `([)]{}`, `({())[]}`, etc.

So the solution is really easy: To verify that each Start Token has a
corresponding End Token (and in correct order!) we should use a stack and
either push new element to the stack in case of Start Token or pop the Token if
it is corresponding End Token. For Example: if stack := `([{` (rightmost is
last), then if next char is `}`, then we pop and stack = `([`, else: push ->
stack (for example `)`), then stack = `([{)`.

Simply adapting our problem to Start and End as well as verifying `name` is the
same will result in us being able to solve this problem.

### Build AST

While we could verify the XmlTokens Iterable and then generate AST using some
hacked solutions, we can also adapt the algorithm to build AST in a single pass

0. stack := []; inter_list := [];
1. next_token := read next token  # I no next token, but inter_list or stack
   are not empty: raise error, else finish
2. if next_token.type = Start -> push it to stack 
3. if next_token.type = SelfClosing -> Build XmlElement and push it to inter_list
4. if next_token.type = End:
    1. if stack.top.name != next_token.name: raise error: mismatching Tokens
    2. else: Build XmlElement and set it's children to inter_list; inter_list = []


## Intermediate Code Generation


