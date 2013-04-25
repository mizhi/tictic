import logging
import random

from .pyparsing import (Literal, Optional, Word, alphas, alphanums, nums,
                        ParseException)

logger = logging.getLogger()

#
# Define parser
#
unit = Word(alphas) + Optional(Literal("/") + Word(alphas))
value = Word(nums).setParseAction(lambda t: int(t[0]))
to_be = Literal("is") | Literal("was") | Literal("=")
variable = Word(alphas, alphanums + "_")
possessive = Literal("my")
update_phrase = Optional(possessive) + \
                variable.setResultsName("variable") + \
                Optional(to_be) + \
                value.setResultsName("value") + \
                Optional(unit).setResultsName("units")

def parse(phrase = None):
    if phrase is None:
        return None

    try:
        result = update_phrase.parseString(phrase)
    except ParseException as e:
        logger.debug("Bad parse for '{0}'".format(phrase))
        raise

    return dict(variable = result.variable,
                value = result.value)
