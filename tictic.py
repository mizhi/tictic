import datetime
import jinja2
import os
import webapp2

# some google apis
from google.appengine.api import users

# application apis
from nl import parser
from model import User, Variable, Value
from xmpp import XmppHandler

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

app = webapp2.WSGIApplication([('/_ah/xmpp/message/chat/', XmppHandler),
                               ('/view', ViewStats),
                               ('/', CheckLogin)],
                              debug=True)
