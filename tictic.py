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
from model import Variable

#
# XMPP handler. Probably needs to be in its own module... iteration...
#
# Messages are sent to seggytictic@appspot.com
#
class XmppHandler(xmpp_handlers.CommandHandler):
    def text_message(self, message):
        sender = message.sender.split("/")
        if len(sender) == 2:
            email,clientapp = sender[0],sender[1]
        else:
            email,clientapp = sender[0], None

        message.reply("I see you as {sender}".format(sender = message.sender))

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
