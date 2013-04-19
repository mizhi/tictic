import datetime
import jinja2
import os
import webapp2

# some google apis
from google.appengine.api import users
from google.appengine.api import xmpp
from google.appengine.ext.webapp import xmpp_handlers

# application apis
from nl import parser
from model import User, Variable, Value

#
# XMPP handler. Probably needs to be in its own module... iteration...
#
# Messages are sent to seggytictic@appspot.com
#
class XmppHandler(xmpp_handlers.CommandHandler):
    def forget_command(self, message = None):
        sender = message.sender.split("/")
        if len(sender) == 2:
            email, clientapp = sender[0], sender[1]
        else:
            email, clientapp = sender[0], None

        q = User.all().filter("email = ", email)
        user = q.get()

        if user:
            message.reply("Okay, I'm forgetting you, {sender}.".format(sender = email))
            for variable in user.variables:
                for value in variable.values:
                    value.delete()
                variable.delete()
            user.delete()
        else:
            message.reply("I don't know you.")

    def help_command(self, message = None):
        message.reply("I'm sending you some help.")

    def text_message(self, message):
        sender = message.sender.split("/")
        if len(sender) == 2:
            email, clientapp = sender[0], sender[1]
        else:
            email, clientapp = sender[0], None

        q = User.all().filter("email = ", email)
        user = q.get()

        if not user:
            user = User(email = email)
            user.put()

        datum = parser.parse(message.body)

        variable = Variable(name = datum["variable"], user = user)
        variable.put()

        value = Value(value = datum["value"], variable = variable)
        value.put()

        message.reply("I've logged variable {variable} as being {value}".format(sender = email,
                                                                                variable = datum["variable"],
                                                                                value = datum["value"]))

###


env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(
        os.path.join(os.path.dirname(__file__),
                     "templates")))

class CheckLogin(webapp2.RequestHandler):
    def get(self):
        self.response.write(parser.dummy)

class ViewStats(webapp2.RequestHandler):
    def get(self):
        self.response.write("View stats")

app = webapp2.WSGIApplication([
    ('/_ah/xmpp/message/chat/', XmppHandler),
    ('/view', ViewStats),
    ('/', CheckLogin)],
                              debug=True)
