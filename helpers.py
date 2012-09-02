'''
Created on Sep 1, 2012

@author: Caroline
'''

import webapp2
import jinja2
import os
import re
from datetime import datetime
import time
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext import blobstore
from google.appengine.ext import db
from models import Posts
from google.appengine.api import images
from google.appengine.api import users
from urlparse import urlparse, parse_qs


class MediaHelper():
    def getImageURL(self, blob_key):
        if blob_key:
            return images.get_serving_url(blob_key, size=None, crop=False, secure_url=None)
        else:
            return None
        
    def parseYoutubeId(self, url):
        if url:
            return parse_qs(urlparse(url).query)['v'][0]
        else:
            return None
        
class PostFilter():
    def loadMainPage(self, queryStr):
        #TODO: paging
        q = db.GqlQuery(queryStr)
        #TODO make configurable in settings
        posts = q.fetch(10)
           
        dictImg = {}
        dictVidId = {}
        for post in posts:
            #get image location
            blob_url = MediaHelper().getImageURL(post.blob_key)
            dictImg[post] = blob_url
            #parse youtube url
            dictVidId[post] = MediaHelper().parseYoutubeId(post.video_url)
        return {'notes': posts, 'img' : dictImg, 'video' : dictVidId}  

        
    def send_error(self, field, subject, content):
        pass
