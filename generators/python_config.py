from enum import Enum, auto

class Token(Enum):
    Comment = auto()
    Variable = auto()
    Constant = auto()
    Numeric = auto()
    Operator = auto()
    Namespace = auto()
    Function = auto()
    Control = auto()
    Whitespace = auto()

# TODO: Find a better way to do this

class Symbol:
    ALL: "list[Symbol]" = []

    def __init__(self, name: str, pattern: str, token: Token, avg_length: int = 1) -> None:
        self.name = name
        self.pattern = pattern
        self.token = token
        self.avg_length = avg_length
        Symbol.ALL.append(self)

Indent1 = Symbol("Indent1", " ", Token.Whitespace)
Indent2 = Symbol("Indent2", " ", Token.Whitespace)
Indent3 = Symbol("Indent3", " ", Token.Whitespace)
Indent4 = Symbol("Indent4", " ", Token.Whitespace)
LastIndent1 = Symbol("LastIndent1", " ", Token.Whitespace)
LastIndent2 = Symbol("LastIndent2", " ", Token.Whitespace)
LastIndent3 = Symbol("LastIndent3", " ", Token.Whitespace)
LastIndent4 = Symbol("LastIndent4", " ", Token.Whitespace)

Continued = Symbol("Continued", "", Token.Comment) # Special. Use when not finishing the line.
EOL = Symbol("EOL", " ", Token.Whitespace)
Comment1 = Symbol("Comment1", " ", Token.Whitespace)
Comment2 = Symbol("Comment2", "#", Token.Comment)
Comment3 = Symbol("Comment3", " ", Token.Comment)
Comment = Symbol("Comment", "[\\w ]", Token.Comment, 10)

ForF = Symbol("ForF", "f", Token.Control)
ForO = Symbol("ForO", "o", Token.Control)
ForR = Symbol("ForR", "r", Token.Control)
For1 = Symbol("For1", " ", Token.Whitespace)
WhileW = Symbol("WhileW", "w", Token.Control)
WhileH = Symbol("WhileH", "h", Token.Control)
WhileI = Symbol("WhileI", "i", Token.Control)
WhileL = Symbol("WhileL", "l", Token.Control)
WhileE = Symbol("WhileE", "e", Token.Control)
While1 = Symbol("While1", " ", Token.Whitespace)
IfI = Symbol("IfI", "i", Token.Control)
IfF = Symbol("IfF", "f", Token.Control)
If1 = Symbol("If1", " ", Token.Whitespace)

InVar = Symbol("InVar", "[A-Za-z]", Token.Variable, 3)
In1 = Symbol("In1", " ", Token.Whitespace)
InI = Symbol("InI", "i", Token.Control)
InN = Symbol("InN", "n", Token.Control)
In2 = Symbol("In2", " ", Token.Whitespace)
LoopVar = Symbol("LoopVar", "[A-Za-z]", Token.Variable, 3)
LoopConst = Symbol("LoopConst", "[A-Z0-9_]", Token.Constant, 5)
RangeR = Symbol("RangeR", "r", Token.Namespace)
RangeA = Symbol("RangeA", "a", Token.Namespace)
RangeN = Symbol("RangeN", "n", Token.Namespace)
RangeG = Symbol("RangeG", "g", Token.Namespace)
RangeE = Symbol("RangeE", "e", Token.Namespace)
Range1 = Symbol("Range1", "\\(", Token.Operator)
RangeNum = Symbol("RangeNum", "\\d", Token.Numeric, 3)
Range2 = Symbol("Range2", "\\)", Token.Operator)

ConditionVar1 = Symbol("ConditionVar1", "[A-Za-z]", Token.Variable, 3)
Condition1 = Symbol("Condition1", " ", Token.Whitespace)
ConditionLess = Symbol("ConditionLess", "<", Token.Operator)
ConditionGreater = Symbol("ConditionGreater", ">", Token.Operator)
ConditionDifferent = Symbol("ConditionDifferent", "!", Token.Operator)
ConditionEqual = Symbol("ConditionEqual", "=", Token.Operator)
Condition = Symbol("Condition", "=", Token.Operator)
Condition2 = Symbol("Condition2", " ", Token.Whitespace)
ConditionVar2 = Symbol("ConditionVar2", "[A-Za-z]", Token.Variable, 3)
ConditionConst = Symbol("ConditionConst", "[A-Za-z]", Token.Variable, 3)
ConditionNum = Symbol("ConditionNum", "\\d", Token.Numeric, 3)

Colon = Symbol("Colon", ":", Token.Operator)

AssignationVar1 = Symbol("AssignationVar1", "[A-Za-z]", Token.Variable, 3)
Assignation1 = Symbol("Assignation1", " ", Token.Whitespace)
AssignationEq = Symbol("AssignationEq", "=", Token.Operator)
Assignation2 = Symbol("Assignation2", " ", Token.Whitespace)
AssignationVar2 = Symbol("AssignationVar2", "[A-Za-z]", Token.Variable, 3)



PHRASES: list[list[Symbol]] = [
    # # Comment
    [Comment2, Comment3, Comment, Comment],
    # var1 = var2
    [AssignationVar1, Assignation1, AssignationEq, Assignation2, AssignationVar2],
    # ... var in range(num):
    [InVar, In1, InI, InN, In2, RangeR, RangeA, RangeN, RangeG, RangeE, Range1, RangeNum, Range2, Colon],
    # ... var1 in var2:
    [In2, LoopVar, Colon],
    # ... var in CONST:
    [In2, LoopConst, Colon],
    # ... var1 ?= var2;
    [ConditionVar1, Condition1, ConditionEqual, Condition, Condition2, ConditionVar2, Colon],
    [Condition1, ConditionDifferent, Condition, Condition2],
    [Condition1, ConditionGreater, Condition2],
    [Condition1, ConditionGreater, Condition, Condition2],
    [Condition1, ConditionLess, Condition2],
    [Condition1, ConditionLess, Condition, Condition2],
    # while ...
    [WhileW, WhileI, WhileL, WhileE, While1, InVar, Continued],
    [WhileW, WhileI, WhileL, WhileE, While1, ConditionVar1, Continued],
    # for ...
    [ForF, ForO, ForR, For1, InVar, Continued],
    [ForF, ForO, ForR, For1, ConditionVar1, Continued],
    # if ...
    [IfI, IfF, If1, InVar, Continued],
    [IfI, IfF, If1, ConditionVar1, Continued],
]

FORCED = {
    Indent1: {
        "up": [
            symbol for symbol in Symbol.ALL
            if symbol not in (Indent2, Indent3, Indent4, LastIndent2, LastIndent3, LastIndent4)
        ]
    },
    ForF: {
        "down": [LastIndent1],
    },
    WhileW: {
        "down": [LastIndent1],
    },
    IfI: {
        "down": [LastIndent1],
    }
}

# Add comments
COMMENT_PHRASE = [Comment1, Comment2, Comment3, Comment, Comment]
for phrase in PHRASES.copy():
    if phrase[-1] == Continued:
        phrase.pop(-1)
        continue
    if Comment not in phrase:
        PHRASES.append(phrase + COMMENT_PHRASE)

# Add indents and EOL
PHRASES = [[LastIndent4] + phrase + [EOL, EOL]]
PHRASES.append([Indent4, Indent1, Indent2, Indent3, Indent4, LastIndent1, LastIndent2, LastIndent3, LastIndent4])