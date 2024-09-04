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

    def __init__(self, name: str, pattern: str, token: Token, weight: int = 1) -> None:
        self.name = name
        self.pattern = pattern
        self.token = token
        self.weight = weight
        Symbol.ALL.append(self)

# Indent1 = Symbol("Indent1", " ", Token.Whitespace)
# Indent2 = Symbol("Indent2", " ", Token.Whitespace)
# Indent3 = Symbol("Indent3", " ", Token.Whitespace)
# Indent4 = Symbol("Indent4", " ", Token.Whitespace)

EOL = Symbol("EOL", " ", Token.Whitespace)
Comment1 = Symbol("Comment1", " ", Token.Whitespace)
Comment2 = Symbol("Comment2", "#", Token.Comment)
Comment3 = Symbol("Comment3", " ", Token.Comment)
Comment = Symbol("Comment", ".", Token.Comment)

# ForF = Symbol("ForF", "f", Token.Control)
# ForO = Symbol("ForO", "o", Token.Control)
# ForR = Symbol("ForR", "r", Token.Control)
# For1 = Symbol("For1", " ", Token.Whitespace)
# ForVar = Symbol("ForVar", "\\w", Token.Variable)
# For2 = Symbol("For2", " ", Token.Whitespace)
# ForI = Symbol("ForI", "i", Token.Control)
# ForN = Symbol("ForN", "n", Token.Control)
# For3 = Symbol("For3", " ", Token.Whitespace)

# WhileW = Symbol("WhileW", "w", Token.Control)
# WhileH = Symbol("WhileH", "h", Token.Control)
# WhileI = Symbol("WhileI", "i", Token.Control)
# WhileL = Symbol("WhileL", "l", Token.Control)
# WhileE = Symbol("WhileE", "e", Token.Control)
# While1 = Symbol("While1", " ", Token.Whitespace)

# LoopVar = Symbol("LoopVar", "\\w", Token.Variable)
# LoopConst = Symbol("LoopConst", "[A-Z0-9_]", Token.Constant)
# RangeR = Symbol("RangeR", "r", Token.Namespace)
# RangeA = Symbol("RangeA", "a", Token.Namespace)
# RangeN = Symbol("RangeN", "n", Token.Namespace)
# RangeG = Symbol("RangeG", "g", Token.Namespace)
# RangeE = Symbol("RangeE", "e", Token.Namespace)
# Range1 = Symbol("Range1", "(", Token.Operator)
# RangeNum = Symbol("RangeNum", "\\d", Token.Numeric)
# Range2 = Symbol("Range2", ")", Token.Operator)
# LoopEnd = Symbol("LoopEnd", ":", Token.Operator)

AssignationVar1 = Symbol("AssignationVar1", "\\w", Token.Variable)
Assignation1 = Symbol("Assignation1", " ", Token.Whitespace, 20)
AssignationEq = Symbol("AssignationEq", "=", Token.Operator, 20)
Assignation2 = Symbol("Assignation2", " ", Token.Whitespace, 20)
AssignationVar2 = Symbol("AssignationVar2", "\\w", Token.Variable)



NEW_INDENT_BELOW: list[Symbol] = [
    # ForF,
    # WhileW,
]

PHRASES: list[list[Symbol]] = [
    [AssignationVar1, AssignationVar1, Assignation1, AssignationEq, Assignation2, AssignationVar2, AssignationVar2, EOL],
]