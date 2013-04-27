# Copyright (c) - 2013 Mitchell Peabody.
# See COPYRIGHT.txt and LICENSE.txt in the root of this project.
from functools import wraps
import inspect
import logging

from google.appengine.api import xmpp, users
from google.appengine.ext.webapp import xmpp_handlers


from model import User, Variable, Value
from nl import parser

logger = logging.getLogger()

def extract_email(sender):
    """XMPP sender is <address>/<client>. I think. This may be wrong, but that's
    what it appears like in GoogleTalk.

    :param xmpp_sender: The sender of the message.
    :returns: email of the sender
    """
    email = sender.split("/")
    return email[0]

def describe(description, params = ""):
    def _describe(func):
        setattr(func, "__command_help__",
                "/{0} {1}\n\t{2}".format(func.__name__.replace("_command", ""),
                                         params,
                                         description))
        return func
    return _describe


class XmppHandler(xmpp_handlers.CommandHandler):
    @describe("Disremembers the user.")
    def forget_command(self, message = None):
        email = extract_email(message.sender)

        try:
            sender = users.User(email)
        except users.UserNotFoundError as e:
            message.reply("You don't seem to have an account that I can find.")

        appuser = User.all().filter("info = ", sender).get()

        if appuser:
            message.reply("Okay, I'm forgetting you, {sender}.".format(sender = sender.email()))
            for variable in user.variables:
                for value in variable.values:
                    value.delete()
                variable.delete()
            appuser.delete()
        else:
            message.reply("I don't know you.")

    @describe("Give help for the system.")
    def help_command(self, message = None):
        """Returns a list of all the commands defined on this class.
        """
        members = [x[1] for x in inspect.getmembers(self, inspect.ismethod)
                   if x[0].endswith("_command") and hasattr(x[1], "__command_help__")]

        reply = "\n".join(map(lambda x: getattr(x, "__command_help__"),
                              members))

        message.reply(reply)

    def text_message(self, message):
        email = extract_email(message.sender)

        try:
            sender = users.User(email)
        except users.UserNotFoundError as e:
            message.reply("You don't seem to have an account that I can find.")

        appuser = User.all().filter("info = ", sender).get()

        if not appuser:
            appuser = User(info = sender)
            appuser.put()

        try:
            datum = parser.parse(message.body)
        except parser.ParseException as e:
            message.reply("I couldn't understand you. (Message was: {msg})".format(msg = e.message))

        variable = Variable.all().filter("name = ", datum["variable"]).get()
        if not variable:
            variable = Variable(name = datum["variable"], user = appuser)
            variable.put()

        value = Value(value = datum["value"], variable = variable)
        value.put()

        message.reply("I've logged variable {variable} as being {value}".format(sender = email,
                                                                                variable = datum["variable"],
                                                                                value = datum["value"]))
