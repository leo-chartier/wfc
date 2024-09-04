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

class Symbol(Enum):
    # Indent1 = (" ", Token.Whitespace)
    # Indent2 = (" ", Token.Whitespace)
    # Indent3 = (" ", Token.Whitespace)
    # Indent4 = (" ", Token.Whitespace)

    EOL = (" ", Token.Whitespace)
    # Comment1 = (" ", Token.Whitespace)
    # Comment2 = ("#", Token.Comment)
    # Comment3 = (" ", Token.Comment)
    # Comment = (".", Token.Comment)

    # ForF = ("f", Token.Control)
    # ForO = ("o", Token.Control)
    # ForR = ("r", Token.Control)
    # For1 = (" ", Token.Whitespace)
    # ForVar = ("\\w", Token.Variable)
    # For2 = (" ", Token.Whitespace)
    # ForI = ("i", Token.Control)
    # ForN = ("n", Token.Control)
    # For3 = (" ", Token.Whitespace)

    # WhileW = ("w", Token.Control)
    # WhileH = ("h", Token.Control)
    # WhileI = ("i", Token.Control)
    # WhileL = ("l", Token.Control)
    # WhileE = ("e", Token.Control)
    # While1 = (" ", Token.Whitespace)

    # LoopVar = ("\\w", Token.Variable)
    # LoopConst = ("[A-Z0-9_]", Token.Constant)
    # RangeR = ("r", Token.Namespace)
    # RangeA = ("a", Token.Namespace)
    # RangeN = ("n", Token.Namespace)
    # RangeG = ("g", Token.Namespace)
    # RangeE = ("e", Token.Namespace)
    # Range1 = ("(", Token.Operator)
    # RangeNum = ("\\d", Token.Numeric)
    # Range2 = (")", Token.Operator)
    # LoopEnd = (":", Token.Operator)

    AssignationVar1 = ("\\w", Token.Variable)
    Assignation1 = (" ", Token.Whitespace)
    AssignationEq = ("=", Token.Operator)
    Assignation2 = (" ", Token.Whitespace)
    AssignationVar2 = ("\\w", Token.Variable)

    @property
    def pattern(self) -> str:
        return self.value[0]
    
    @property
    def token(self) -> Token:
        return self.value[1]
    
    @property
    def weight(self) -> int:
        if len(self.value) > 2:
            return self.value[3]
        return 1

class Multiple:
    # One or more of this symbol
    def __init__(self, symbol: Symbol) -> None:
        self.symbol = symbol



NEW_INDENT_BELOW = [
    # Symbols.ForF,
    # Symbols.WhileW,
]

EOL = Multiple(Symbol.EOL)
PHRASES = [
    [Multiple(Symbol.AssignationVar1), Symbol.Assignation1, Symbol.AssignationEq, Symbol.Assignation2, Multiple(Symbol.AssignationVar2), EOL],
]