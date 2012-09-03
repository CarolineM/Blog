'''
Created on Sep 1, 2012

@author: Caroline
'''
from google.appengine.ext import db
from models import Posts
from google.appengine.api import images
from urlparse import urlparse, parse_qs

class Callable:

    def __init__(self, anycallable):
        self.__call__ = anycallable

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
    mainarea = None
    page_size = None 
    curr_page_num = 0

    def __init__(self):
        #init vars
        if not PostFilter.mainarea:
            self.setMainarea(self, 'esl_page')
        if not PostFilter.page_size:
            self.setPagesize(self, 10)
    
    def loadMainPage(self, area, pagenum, *saved):
        if not area:
            area = self.mainarea
        
        if area == 'all':
            q = db.GqlQuery("SELECT * FROM Posts WHERE status='Published' ORDER BY date DESC")
        elif not saved:
            q = db.GqlQuery("SELECT * FROM Posts WHERE status='Published' AND " + area + "=TRUE ORDER BY date DESC")
        else:
            q = db.GqlQuery("SELECT * FROM Posts WHERE status='Saved' ORDER BY date DESC")
            
        if pagenum:
            self.curr_page_num = int(pagenum) 
        posts = q.fetch(self.page_size + 1, self.curr_page_num * self.page_size)
        if len(posts) == self.page_size + 1:
            isNext = True
            posts = posts[:self.page_size]
        else:
            isNext = False
        
        if self.curr_page_num > 0:
            isPrev = True
        else: 
            isPrev = False
           
        dictImg = {}
        dictVidId = {}
        for post in posts:
            #get image location
            blob_url = MediaHelper().getImageURL(post.blob_key)
            dictImg[post] = blob_url
            #parse youtube url
            dictVidId[post] = MediaHelper().parseYoutubeId(post.video_url)
        return {'notes': posts, 'img' : dictImg, 'video' : dictVidId, 
                'pagenum' : self.curr_page_num, 'isNext' : isNext, 
                'isPrev' : isPrev}
   
    def setMainarea(self, value):
        PostFilter.mainarea = value  
    
   
    def setPagesize(self, value):
        PostFilter.page_size = value
    
    #get = Callable(get)
    setMainarea = Callable(setMainarea)
    setPagesize = Callable(setPagesize)
        
    #TODO limit 1000, could be done better with cursors
    def totalPosts(self):
        return Posts.all().filter('status', 'Published').count()
        
    def send_error(self, field, subject, content):
        pass
