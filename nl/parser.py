import random

from .pyparsing import Word


# update_phrase = <nl_phrase>
# nl_phrase = [<possessive>] <variable> [<to_be>] <value> [<unit>]
# possessive = "my"
# variable = ([A-Za-z_][A-Za-z]+\w)+
# to_be = "is" | "was" | "="
# value = <number>
# number = [0-9]+
# unit = [A-Za-z]+["/"[A-Za-z]+]

dummy = "This does nothing."


def parse(phrase = None):
    return dict(variable = "test",
                value = random.randint(0,100))
