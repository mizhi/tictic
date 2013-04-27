# Copyright (c) - 2013 Mitchell Peabody.
# See COPYRIGHT.txt and LICENSE.txt in the root of this project.

# google datastore apis
from google.appengine.ext import db

class User(db.Model):
    info = db.UserProperty()

class Variable(db.Model):
    user = db.ReferenceProperty(User,
                                collection_name="variables")
    name = db.StringProperty(required=True)

class Value(db.Model):
    variable = db.ReferenceProperty(Variable,
                                    collection_name="values")
    logged_at = db.DateTimeProperty(auto_now_add=True, indexed=True)
    value = db.IntegerProperty(required=True)
