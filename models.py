'''
Created on May 3, 2012

@author: Caroline
'''
from datetime import datetime
from google.appengine.ext import db
from google.appengine.ext import blobstore


class Posts(db.Model):

    title = db.StringProperty()
    text = db.TextProperty()
    status = db.StringProperty()
    date = db.DateTimeProperty(default=datetime.today())
    video_url = db.StringProperty()
    blob_key = blobstore.BlobReferenceProperty(default=None)
    