from extended import Bool, SignedNum

COMMANDS = ["~", "$", "+", "=", "%", ":", "&", "!", ".",
            "@", "\"", "1", "#", "?", "/", "\\", "|", ">", "<"]

# min | max
ARG_NUM = {
    "~": [1, 1],

    "$": [2, 2],
    "+": [2, 2],
    "=": [2, 2],
    "%": [3, 3],
    ":": [2, 2],
    "&": [2, 2],
    "$": [2, 2],
    "!": [1, 1],
    ".": [1, 1],
    "@": [3, 3],

    "\"": [2, 2],
    "1": [2, 2],

    "#": [1, 1],
    "?": [2, 3],

    "/": [1, None],  # `None` specifies unlimited arguments
    "\\": [0, 1],
    "|": [1, None],

    ">": [1, 1],
    "<": [1, 1],
}

# using an enum so we can make use of bitwise operations for checking types instead of strings


class Types:
    # LT = literal - a literal string is an actual string wrapped in quotes
    # a literal number is just a number
    # a literal bool is `true` / `false`
    LT_NUMBER = 0
    LT_NUMBER_P = 1  # P and N -> positive / negative
    LT_NUMBER_N = 2
    LT_STRING = 4
    LT_BOOL = 8

    # KW = keyword - keywords are `num`, `str`, `bool`
    # they are the types of the variable
    KW_NUMBER = 16
    KW_STRING = 32
    KW_BOOL = 64

    VARIABLE = 128

    ANY_NUMBER = LT_NUMBER | LT_NUMBER_P | LT_NUMBER_N | KW_NUMBER
    ANY_STRING = LT_STRING | KW_STRING

    ANY_VAR = KW_NUMBER | KW_STRING | KW_BOOL

    ANY = KW_NUMBER | KW_STRING | KW_BOOL | LT_NUMBER | LT_NUMBER_P | LT_NUMBER_N | LT_STRING | LT_BOOL

    LITERAL_TO_VAR = {
        LT_STRING: KW_STRING,
        LT_NUMBER: KW_NUMBER,
        LT_BOOL: KW_BOOL,
    }

    def to_string(t: int) -> str:
        return {
            Types.LT_NUMBER: "NUMBER",
            Types.LT_NUMBER_P: "NUMBER",
            Types.LT_NUMBER_N: "NUMBER",

            Types.LT_STRING: "STRING",
            Types.LT_BOOL: "BOOL",

            Types.KW_STRING: "STR_VAR",
            Types.KW_NUMBER: "NUM_VAR",
            Types.KW_BOOL: "BOOL_VAR",

            Types.VARIABLE: "VAR",

            Types.ANY_NUMBER: "ANY_NUMBER",
            Types.ANY_STRING: "ANY_STRING",
            Types.ANY_VAR: "ANY_VAR",
            Types.ANY: "ANY",
        }[t]

    def eq(t1: int, t2: int) -> bool:
        if(isinstance(t1, str) or isinstance(t2, str)):
            return
        return (t1 & t2) > 0


ARG_TYPES = {
    "~": [Types.LT_STRING],

    "$": [Types.VARIABLE, Types.ANY_VAR],
    "+": [Types.KW_NUMBER, Types.ANY_NUMBER],
    "=": [Types.KW_NUMBER, Types.ANY_NUMBER],
    "%": [Types.ANY, Types.ANY, Types.KW_NUMBER],
    ":": [Types.KW_STRING, Types.ANY_STRING],
    "&": [Types.KW_STRING, Types.ANY],
    "!": [Types.ANY_VAR],
    ".": [Types.KW_STRING],

    "@": [Types.KW_STRING | Types.KW_NUMBER, Types.ANY_NUMBER, Types.ANY_NUMBER],

    "\"": [Types.ANY_VAR, Types.KW_STRING],
    "1": [Types.ANY_VAR, Types.KW_NUMBER],

    "#": [Types.LT_NUMBER],
    "?": [Types.ANY_VAR, Types.LT_NUMBER, Types.LT_NUMBER],

    "/": [Types.VARIABLE],
    "\\": [Types.ANY_VAR],
    "|": [Types.VARIABLE, Types.ANY_VAR],

    ">": [Types.ANY_VAR],
    "<": [Types.ANY_VAR],
}

DEFAULT_VALUES = {
    "num": SignedNum(0),
    "str": "",
    "bool": Bool(False),
}
