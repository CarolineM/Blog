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
    esl_page = db.BooleanProperty(default=False)
    life_page = db.BooleanProperty(default=False)
    de_page = db.BooleanProperty(default=False)
    phil_page = db.BooleanProperty(default=False)
    gen_page = db.BooleanProperty(default=False)
    
class Home_Page(db.Model):
    #todo - a better way to save the settings. this is not used yet
    home_page = db.StringProperty(default="gen_page")
    page_size = db.IntegerProperty(default=10)