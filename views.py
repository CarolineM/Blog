'''
Created on May 3, 2012

@author: Caroline
'''


import webapp2
import jinja2
import os
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext import blobstore
from google.appengine.ext import db
from models import Posts


TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')
jinja_environment = jinja2.Environment(loader = jinja2.FileSystemLoader(TEMPLATE_DIR), autoescape=False)


class BaseHandler(webapp2.RequestHandler):
    def render_template(
        self,
        filename,
        template_values={}):
        template = jinja_environment.get_template(filename)
        self.response.out.write(template.render(**template_values))


class MainPage(BaseHandler):
    def get(self):
        posts = Posts.all()
        posts.order("-date")
        self.render_template('index.html', {'notes': posts})


class PostHandler(BaseHandler):
    def send_error(self, field, subject, content):
        self.render_template('post.html', {})

    def post(self):
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
                  status=post_stat    
                  )
        else:
            post = db.get(self.request.get('id'))
            post.title = post_sub
            post.text = post_content
            post.status = post_stat  
                                  
        post.put()
        return webapp2.redirect('/')

    def get(self):
        upload = blobstore.create_upload_url_async('/post')
        if self.request.GET.get('id', None):
            key = self.request.get('id')
            post = db.get(key)
            text = post.text
            title = post.title
            upload_title = "Change Picture:"
            self.render_template('post.html', {'text' : text, 'title' : title, 'id' : key, 
                                               'picUploadLabel' : upload_title, 'upload_url' : upload})
        else:
            upload_title = "Include Picture:"    
            self.render_template('post.html', {'picUploadLabel' : upload_title, 'upload_url' : upload})


class DeletePost(BaseHandler):

    def get(self, note_id):
        iden = int(note_id)
        note = db.get(db.Key.from_path('Notes', iden))
        db.delete(note)
        return webapp2.redirect('/')
