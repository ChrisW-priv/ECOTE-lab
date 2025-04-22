## Scanner State Transition

In my implementation there are following tokens present:

- WS - whitespace, tabs, newline char (ignored)
- SYMBOL - special meaning character: SYMBOLS := \[ "<", "/>", ">", "/>", "=" \]
- TEXT - free text that is just floating around, can be composed by alpha characters or "_"
- STRING - text composed by ANY character, except: STR_BREAK := \[ "\n", EOF \]. This string of characters MUST be wrapped by quotes

The scanner utilizes the `StateTransition` class to manage state changes, implementing a state machine that enforces the defined transitions and rules. This approach ensures robust handling of various input scenarios and prevents errors related to state mismanagement.

### Scanner State Transition

In my implementation, the scanner operates as a state machine managed by the `StateTransition` class. This design encapsulates the state handling logic, making the scanner modular and maintainable.

The scanner recognizes the following tokens:

- **WS**: Whitespace characters (spaces, tabs, newlines) are ignored.
- **SYMBOL**: Special characters with predefined meanings: `<`, `/>`, `>`, `/`, `=`
- **TEXT**: Alphanumeric text and underscores (`_`)
- **STRING**: Any characters except newline and end-of-file (`EOF`), enclosed in quotes

**StateMachine Integration:**

- **`START_STATE`**: Initiates scanning and handles transitions based on the input character.
- **`TEXT_INPUT`**: Accumulates alphanumeric characters and underscores.
- **`SYMBOL_INPUT`**: Processes special symbols, utilizing `StateTransition` to validate symbol sequences.
- **`STRING_INPUT`**: Collects characters within quotes, ensuring proper termination.
- **`STRING_END`**: Finalizes string tokens and handles post-string transitions.

**State Transition Rules:**

- **START_STATE:**
  - On **WS**: Remain in `START_STATE`
  - On **alpha**: Transition to `TEXT_INPUT`
  - On **"<"**, **">"**, **"/"**, **"="**: Transition to `SYMBOL_INPUT`
  - On **'"'**: Transition to `STRING_INPUT`
  - On **numeric characters**: Raise `UnexpectedNumericError`
  
- **TEXT_INPUT:**
  - On **alpha** or **"_"**: Remain in `TEXT_INPUT` and append character
  - On **WS**: Transition to `START_STATE` and emit accumulated `TEXT` token
  - On **SYMBOL characters**: Transition to `SYMBOL_INPUT` and emit accumulated `TEXT` token
  - On **"/"**: Raise `UnexpectedSlashError`
  
- **SYMBOL_INPUT:**
  - On characters forming valid symbols: Append and validate using `StateTransition`
  - On **alpha**: Transition to `TEXT_INPUT` and emit accumulated `SYMBOL` token
  - On **'"'**: Transition to `STRING_INPUT` and emit accumulated `SYMBOL` token
  - On **invalid characters**: Raise `InvalidTransitionError`
  
- **STRING_INPUT:**
  - On **non-terminating characters**: Remain in `STRING_INPUT` and append character
  - On **'"'**: Transition to `STRING_END`
  
- **STRING_END:**
  - On **WS**: Emit `STRING` token and transition to `START_STATE`
  - On **invalid characters**: Raise `QuoteFollowedByNonWhitespaceError`



## Parser State Transition

The parser employs the `StateTransition` class to manage state transitions, implementing a state machine that processes atomic tokens into structured XML tokens and ultimately builds the Abstract Syntax Tree (AST). This structured approach facilitates error handling and ensures compliance with the defined grammar rules.

### Parser State Transition

In my implementation, the parser functions as a state machine governed by the `StateTransition` class. This design allows for systematic processing of tokens and adheres to the grammar specifications.

#### Build XML Tokens

The parser converts atomic tokens from the scanner into larger XML tokens using the following patterns:

- **ATTRIBUTE**: `TEXT(*) SYMBOL(=) STRING(*)`
- **StartToken**: `SYMBOL(<) TEXT(*) ATTRIBUTE* SYMBOL(>)`
- **EndToken**: `SYMBOL(</) TEXT(*) SYMBOL(>)`
- **SelfClosingToken**: `SYMBOL(<) TEXT(*) ATTRIBUTE* SYMBOL(/>)`

**StateMachine Integration:**

- **`START_STATE`**: Awaits the beginning of an XML element.
- **`ELEMENT_START`**: Captures the start of an element and its attributes.
- **`ATTRIBUTE_SET`**: Processes attribute assignments.
- **`ELEMENT_END`**: Handles the closing of elements.
- **`SELF_CLOSING`**: Manages self-closing tags.

**State Transition Rules:**

- **START_STATE:**
  - On **`<`**: Transition to `ELEMENT_START`
  - Else: Raise `InvalidTransitionError`
  
- **ELEMENT_START:**
  - On **TEXT**: Assign as element name and transition to `ATTRIBUTE_SET`
  - Else: Raise `InvalidTransitionError`
  
- **ATTRIBUTE_SET:**
  - On **`=`**: Transition to `ATTRIBUTE_SET_VALUE`
  - On **`>`**: Emit `StartToken` and transition to `IN_DOCUMENT`
  - On **`/>`**: Emit `SelfClosingToken` and transition to `IN_DOCUMENT`
  - Else: Raise `InvalidTransitionError`
  
- **ATTRIBUTE_SET_VALUE:**
  - On **STRING**: Assign attribute value and transition back to `ATTRIBUTE_SET`
  - Else: Raise `InvalidTransitionError`
  
- **ELEMENT_END:**
  - On **TEXT**: Assign as closing element name and transition to `ELEMENT_END_VERIFY`
  - Else: Raise `InvalidTransitionError`
  
- **ELEMENT_END_VERIFY:**
  - On **`>`**: Emit `EndToken` and transition to `IN_DOCUMENT`
  - Else: Raise `InvalidTransitionError`

#### Build AST

Using the structured XML tokens, the parser constructs the AST while ensuring syntactic correctness through the state machine rules.

**Example Transformation:**

```xml
<root>
    <kitten Name="Whiskers">
        <parent>
            <cat Name="The Garfield"/>
        </parent>
    </kitten>
</root>
```

Transforms into the following AST:

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
                }
            ],
            "children": [
                {
                    "element_name": "parent",
                    "children": [
                        {
                            "element_name": "cat",
                            "attributes": [
                                {
                                    "name": "Name",
                                    "value": "The Garfield"
                                }
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

1. Turn atomic tokens into larger, xml tokens 
2. Turn xml tokens into AST

Additional benefit is that the error handling becomes a lot easier just because
we focus on one task at a time.

### Build xml tokens

Now that we have our TOKENS defined, it is time to define the transitions on
those tokens. In my mind, it is way easier to first strongly define our grammar
using the regular expressions.

We will start by defining ATTRIBUTE pattern:

- `ATTRIBUTE` := TEXT(*) SYMBOL(=) STRING(*)

and now, we can use it to define ELEMENT pattern. But there is more than one!
So we will start with a basics:

- `StartToken` := SYMBOL(<) TEXT(*) ATTRIBUTE* SYMBOL(>)
- `EndToken` := SYMBOL(<) TEXT(*) SYMBOL(>)

and now, let us define the ELEMENT:

- ELEMENT := ELEMENT_START ELEMENT* ELEMENT_END  # This we will build in AST build phase
- ELEMENT := SYMBOL(<) TEXT(*) ATTRIBUTE* SYMBOL(/>)  # This is SelfClosingToken

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

### Build AST

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

#### Verify the correctness

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

#### Algorithm

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

## Semantic Analyzer

Now that we have created an AST of the XML_Elements, it is time to verify if 
the tree follows rules defined for us:

- Tree starts with root node
- Tree nodes are either "variable" nodes or "declaration" nodes
- immediate child of the "variable" node has to be at least one "declaration"
  node (except for root). Note: while in principle, we COULD have a chain of 
  "variable" nodes, that would creation of a "List of lists" structure which we
  disallow in the assumptions. Note: All nodes except for root follow this 
  rule. In case of root, if there is "variable" node, then it is a list.
- immediate child of the "declaration" node has to be "variable" node 
  (0 or more)

Example:
```xml 
<root>  # Starts with root
    <kitten Name="Whiskers">  # This node has attributes -> "declaration" node
        <Parents>  # This node has no attributes -> "variable" node
            <cat Name="The Garfield"/>  # This node has attributes -> "declaration"
        </Parents>
        <BestFriend>  # This node has no attributes -> "variable" node
            <scout Name="Scout"/>  # This node has attributes -> "declaration"
        </BestFriend>
    </kitten>
    <ppl>  # This node has no attributes -> "variable" node (list) (lenght=1)
        <john Name="John"/>  # This node has attributes -> "declaration"
    </ppl>
    <cars>  # This node has no attributes -> "variable" node (list) (lenght=2)
        <car1 Name="Lightning"/>  # This node has attributes -> "declaration"
        <car2 Name="Sally"/>  # This node has attributes -> "declaration"
    </cars>
    <newman Name="Joseph"/>  # This node has attributes -> "declaration"
    <paul Name="Paul Atreides">  # This node has attributes -> "declaration" node
        <Parents>  # This node has no attributes -> "variable" node. NOTICE: THIS IS A LIST NOW!!!
            <pauls_father Name="Duke Leto Atreides I"/>  # This node has attributes -> "declaration"
            <pauls_mother Name="Lady Jessica"/>  # This node has attributes -> "declaration"
        </Parents>
    </kitten>
</root>
```

Notice: this example explores some tricky edge cases:

- "parents" attribute has a type of `List<Class1>`, even though, we learn about 
  this only at the very end
- All "variable" nodes attribute are `List<Class1>`, even if they have just one 
  element.
- "declaration" nodes are just instances of the class, nothing too strange

Then, since we are already here, and we did the analysis work once, we can 
create new "Typed AST" that will be easier to parse and be guaranteed to follow
intended rules. Proposed Tree:

```json
{
    "element_name": "root",
    "identified_type": "variable",
    "identified_role": null,
    "children": [
        {
            "element_name": "kitten",
            "identified_type": "declaration",
            "identified_role": null,
            "attributes": [
                {
                    "name": "Name",
                    "value": "Whiskers",
                    "": "Whiskers",
                },
            ],
            "children": [
                {
                    "element_name": "Parents",
                    "identified_type": "variable",
                    "identified_role": "attribute_of_parent",
                    "attributes": null,
                    "children": [
                        {
                            "element_name": "cat",
                            "identified_type": "declaration",
                            "identified_role": "value_of_an_attribute",
                            "attributes": [
                                {
                                    "name": "Name",
                                    "value": "The Garfield"
                                },
                            ],
                            "children": null
                        }
                    ]
                },
                {
                    "element_name": "BestFriend",
                    "identified_type": "variable",
                    "identified_role": "attribute_of_parent",
                    "attributes": null,
                    "children": [
                        {
                            "element_name": "scout",
                            "identified_type": "declaration",
                            "identified_role": "value_of_an_attribute",
                            "attributes": [
                                {
                                    "name": "Name",
                                    "value": "Scout"
                                },
                            ],
                            "children": null
                        }
                    ]
                }
            ]
        },
        ...
    ]
}
```

## Intermediate code generation

Now that we have full information on the fact that the AST is indeed correct,
as well as some types of nodes and roles etc. we can proceed to building the 
code. Again, building the code right away is hard, so we will first generate 
some intermediate result, that will be trivial to turn into actual code.

On this step, we will: 

- Identify unique classes and it's types
- Identify all declarations and it's dependencies (references to other
  declaration, that we need to build first and use to build current instance)
  (possibly also save it topological order)


## Code Generation 

When we have the code prepared to be generated, we shall now use it using some
templates. We will not yet save those templates to the filesystem, but instead,
generate a map of filename to file content. This way it will be easier to test 
or change the configuration later.

## Code Write

Finally, when we have all the code, we inspect the configuration and save the 
files to the filesystem.
