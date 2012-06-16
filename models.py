'''
Created on May 3, 2012

@author: Caroline
'''
from google.appengine.ext import db
from google.appengine.ext import blobstore


class Posts(db.Model):

    title = db.StringProperty()
    text = db.TextProperty()
    status = db.StringProperty()
    date = db.DateTimeProperty(auto_now_add=True)
    blob_key = blobstore.BlobReferenceProperty(default=None)
    
class Comments(db.Model):

    author = db.StringProperty(required = True)
    text = db.StringProperty(multiline=True, required = True)
    date = db.DateTimeProperty(auto_now_add=True)