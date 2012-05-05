'''
Created on May 3, 2012

@author: Caroline
'''


import webapp2
import jinja2
import os
from datetime import datetime
from google.appengine.ext import db
from models import Posts


TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')
jinja_environment = jinja2.Environment(loader = jinja2.FileSystemLoader(TEMPLATE_DIR), autoescape=True)


class BaseHandler(webapp2.RequestHandler):
    def render_template(
        self,
        filename,
        template_values,
        **template_args):
        template = jinja_environment.get_template(filename)
        self.response.out.write(template.render(template_values))


class MainPage(BaseHandler):

    def get(self):
        #self.write("test")
        posts = Posts.all()
        posts.order("-date")
        self.render_template('index.html', {'notes': posts})


class CreatePost(BaseHandler):

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
        post = Posts(
                  title=self.request.get('subject'),
                  text=self.request.get('content'),
                  status=post_stat    
                  )
        post.put()
        return webapp2.redirect('/')

    def get(self):
        self.render_template('newpost.html', {})


class EditPost(BaseHandler):

    def post(self, note_id):
        iden = int(note_id)
        note = db.get(db.Key.from_path('Notes', iden))
        note.author = self.request.get('author')
        note.text = self.request.get('text')
        note.priority = self.request.get('priority')
        note.status = self.request.get('status')
        note.date = datetime.now()
        note.put()
        return webapp2.redirect('/')

    def get(self, note_id):
        iden = int(note_id)
        note = db.get(db.Key.from_path('Notes', iden))
        self.render_template('edit.html', {'note': note})


class DeletePost(BaseHandler):

    def get(self, note_id):
        iden = int(note_id)
        note = db.get(db.Key.from_path('Notes', iden))
        db.delete(note)
        return webapp2.redirect('/')
