# Copyright (c) - 2013 Mitchell Peabody.
# See COPYRIGHT.txt and LICENSE.txt in the root of this project.
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

class ViewStats(webapp2.RequestHandler):
    def get(self):
        google_user = users.get_current_user()

        # will have already been authorized by appengine. Look up in our
        # user database
        appuser = User.all().filter("info =", google_user).get()
        if not appuser:
            # no records for this person yet, so tell them to send a message to
            # our bot.
            templ = env.get_template("fail.template.html")
            self.response.write(templ.render(
                dict(user = google_user)
            ))
        else:
            # look up variables
            templ = env.get_template("view.template.html")
            self.response.write(templ.render(
                dict(user = appuser)
            ))

app = webapp2.WSGIApplication([('/_ah/xmpp/message/chat/', XmppHandler),
                               ('/', ViewStats)],
                              debug=True)
