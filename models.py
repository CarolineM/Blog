'''
Created on May 3, 2012

@author: Caroline
'''
from google.appengine.ext import db


class Posts(db.Model):

    title = db.StringProperty(required = True)
    text = db.TextProperty(required = True)
    status = db.StringProperty()
    date = db.DateTimeProperty(auto_now_add=True)
    
class Comments(db.Model):

    author = db.StringProperty(required = True)
    text = db.StringProperty(multiline=True, required = True)
    date = db.DateTimeProperty(auto_now_add=True)