'''
Created on May 3, 2012

@author: Caroline
'''


import webapp2
import jinja2
import os
import re
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext import blobstore
from google.appengine.ext import db
from models import Posts
from google.appengine.api import images
from google.appengine.api import users


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
        posts = Posts.all()
        posts.order("-date")
           
        dictionary = {}
        for post in posts:
            if post.blob_key:
                blob_url = images.get_serving_url(post.blob_key, size=None, crop=False, secure_url=None)
            else:
                blob_url = None
            dictionary[post] = blob_url   
        self.render_template('index.html', {'notes': dictionary,  })
        

class PostHandler(BaseHandler, blobstore_handlers.BlobstoreUploadHandler):
    def send_error(self, field, subject, content):
        self.render_template('post.html', {})

    def post(self):
        upload_files = self.get_uploads('file')
        if upload_files:  
            blob_info = upload_files[0]
            blob_key = blob_info.key()
        else:
            blob_key = None 
             
        is_post = self.request.POST.get('post', None) 
        is_save = self.request.POST.get('save', None)
        post_stat = ""
        if is_post:
            post_stat = "Published"
        elif is_save:
            post_stat = "Saved"
        else: 
            raise Exception('no form action given')
        #error checking
        post_sub = self.request.get('subject')
        post_content = self.request.get('content')
        
        if post_sub == "":
            self.send_error('title', "post.html")
            return
        elif post_content == "":
            self.send_error('content', "post.html")
            return
        
        #no errors, so save/update post
        if not self.request.POST.get('id', None):
            post = Posts(
                  title=post_sub,
                  text=post_content,
                  status=post_stat,
                  blob_key=blob_key   
                  )
        else:
            post = db.get(self.request.get('id'))
            post.title = post_sub
            post.text = post_content
            post.status = post_stat
            if blob_key:
                #TODO: delete BlobInfo.get(post.blob_key) 
                post.blob_key=blob_key  
                                  
        post.put()
        return webapp2.redirect('/')

    def get(self):
        if users.get_current_user():
            upload = blobstore.create_upload_url('/post')
            if self.request.GET.get('id', None):
                key = self.request.get('id')
                post = db.get(key)
                text = post.text
                title = post.title
                upload_title = "Change Picture:"
                self.render_template('post.html', {'text' : text, 'title' : title, 'id' : key, 
                                               'picUploadLabel' : upload_title, 'upload_url' : upload, 'users' : users })
            else:
                upload_title = "Include Picture:"    
                self.render_template('post.html', {'picUploadLabel' : upload_title, 'upload_url' : upload, 'users' : users })
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
    def get(self, note_id):
        iden = int(note_id)
        note = db.get(db.Key.from_path('Notes', iden))
        db.delete(note)
        return webapp2.redirect('/')
