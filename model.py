# google datastore apis
from google.appengine.ext import db

class User(db.Model):
    email = db.EmailProperty()

class Variable(db.Model):
    user = db.ReferenceProperty(User,
                                collection_name="variables")
    name = db.StringProperty(required=True)

class Value(db.Model):
    variable = db.ReferenceProperty(Variable,
                                    collection_name="values")
    logged_at = db.DateTimeProperty(auto_now_add=True)
    value = db.IntegerProperty(required=True)
