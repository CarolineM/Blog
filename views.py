'''
Created on May 3, 2012

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
from google.appengine.api import users
from urlparse import urlparse, parse_qs
from helpers import MediaHelper, PostFilter


TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')
jinja_environment = jinja2.Environment(loader = jinja2.FileSystemLoader(TEMPLATE_DIR), autoescape=False)


class BaseHandler(webapp2.RequestHandler):
    def render_template(
        self,
        filename,
        template_values={}):
        template_values['users'] = users
        if (users.get_current_user()):
            template_values['logout'] = users.CreateLogoutURL('/logout', _auth_domain=None)
        template = jinja_environment.get_template(filename)
        self.response.out.write(template.render(**template_values))


class MainPage(BaseHandler, blobstore_handlers.BlobstoreDownloadHandler):
    def get(self):
        PostFilter().loadManPage()
        

class PostHandler(BaseHandler, blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        upload_files = self.get_uploads('file')
        #TODO google.appengine.ext.blobstore.MAX_BLOB_FETCH_SIZE 
        if upload_files:  
            blob_info = upload_files[0]
            blob_key = blob_info.key()
        else:
            blob_key = None 
             
        is_post = self.request.get('post', None) 
        is_save = self.request.get('save', None)
        post_stat = ""
        if is_post:
            post_stat = "Published"
        elif is_save:
            post_stat = "Saved"
        else: 
            raise Exception('no form action given')
        
        post_sub = self.request.get('subject')
        post_content = self.request.get('content')
        vid_url = self.request.get('video')
        date_str = self.request.get('date')
        
        #error checking TODO         
        if post_sub == "":
            self.send_error('title', "post.html")
            return
        elif post_content == "":
            self.send_error('content', "post.html")
            return        
            
        #make datetime
        if not date_str == None:
            date = datetime.strptime(date_str,'%m/%d/%Y')
            time = datetime.time(datetime.now())
            dt = datetime.combine(date, time)
        else:
            dt = None
        
        #no errors, so save/update post
        if not self.request.POST.get('id', None):
            post = Posts(
                  title=post_sub,
                  text=post_content,
                  status=post_stat,
                  video_url=vid_url,
                  blob_key=blob_key,
                  date=dt   
                  )
        #editing
        else:
            post = db.get(self.request.get('id'))
            post.title = post_sub
            post.text = post_content
            post.status = post_stat
            post.video_url=vid_url
            post.date=dt
            if blob_key and post.blob_key:
                if not post.blob_key == blob_key:
                    blobstore.delete(post.blob_key.key())  
                    post.blob_key=blob_key
            elif blob_key:
                post.blob_key = blob_key
            elif post.blob_key:
                blobstore.delete(post.blob_key.key()) 
        post.put()
        return webapp2.redirect('/')

    def get(self):
        if users.get_current_user():
            upload = blobstore.create_upload_url('/post')
            if self.request.GET.get('post_id', None):
                key = self.request.get('post_id')
                post = db.get(key)
                text = post.text
                title = post.title
                youtube = post.video_url
                image = MediaHelper().getImageURL(post.blob_key)
                date = post.date.strftime('%m/%d/%Y')
                self.render_template('post.html', {'text' : text, 'title' : title, 'id' : key, 
                                                   'upload_url' : upload, 'date' : date, 
                                                   'youtube' : youtube, 'image' : image})
            else:   
                self.render_template('post.html', {'upload_url' : upload })
        else:
            message= "You must login to access this page".encode("utf8")
            self.redirect('/logout?message=' + message)
                    
            
class SignInHandler(BaseHandler):
    def get(self):
        self.redirect(users.create_login_url(dest_url='/userchecker',
                    _auth_domain=None,
                    federated_identity=self.request.get('domain')))
        
class UserCheckerHandler(BaseHandler):
    message = ""
    
    def get(self):
        user = users.get_current_user()
        if user and self.check_email(user):
            self.redirect('/');
        else:
            url = users.CreateLogoutURL('/logout?message=' + self.message, _auth_domain=None)
            self.redirect(url)
            
            
    def check_email(self, user):
            m = re.search('(cmcquatt|adrijdin)@gmail.com', user.email())
            if m:
                self.message = "See you soon!".encode("utf8")
                return True
            else:
                self.message = "You cannot login to this site".encode("utf8")
                return False
            
class LogoutHandler(BaseHandler):
    def get(self):
        message = self.request.get("message")
        self.render_template('logout.html', {'message' : message, 'users' : users })
                    
            
class DeletePost(BaseHandler):
    def post(self):
        post = db.get(self.request.get("post_id"))
        if post.blob_key:
            blobstore.delete_async(post.blob_key.key())
        post.delete()
        self.redirect('/')

class DeleteImage(BaseHandler):
    def post(self):
        post_id = self.request.get("post_id")
        post = db.get(post_id)
        if post.blob_key:
            blobstore.delete_async(post.blob_key.key())
            post.blob_key=None
            post.put()


        
