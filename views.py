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
from helpers import MediaHelper, PostFilter

#TODO video input checking
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


class MainPage(BaseHandler):
        
    def get(self):
        pfilter = PostFilter()
        pageArgs = pfilter.loadMainPage(False, self.request.get("pg"))
        pageArgs['currpage'] = "/"
        self.render_template('index.html', pageArgs)

class AllPage(BaseHandler):
    def get(self):
        if users.get_current_user():
            pageArgs = PostFilter().loadMainPage("all", self.request.get("pg"))
            pageArgs['currpage'] = "/all"
            self.render_template('index.html', pageArgs)
        else:
            message= "You must login to access this page".encode("utf8")
            self.redirect('/logout?message=' + message)

class SavedPage(BaseHandler):
    
    def get(self):
        pageArgs = PostFilter().loadMainPage(False, self.request.get("pg"), True)
        pageArgs['saved'] = True
        pageArgs['currpage'] = "/saved"
        self.render_template('index.html', pageArgs)

class ESLPage(BaseHandler):
    
    def get(self):
        pageArgs = PostFilter().loadMainPage("esl_page", self.request.get("pg"))
        pageArgs['currpage'] = "/esl"
        self.render_template('index.html', pageArgs)

class LifestylePage(BaseHandler):
    
    def get(self):
        pageArgs = PostFilter().loadMainPage("life_page", self.request.get("pg"))
        pageArgs['currpage'] = "/lifestyle"
        self.render_template('index.html', pageArgs)

class PhilosophyPage(BaseHandler):
    
    def get(self):
        pageArgs = PostFilter().loadMainPage("phil_page", self.request.get("pg"))
        pageArgs['currpage'] = "/philosophy"
        self.render_template('index.html', pageArgs)

class GeneralPage(BaseHandler):
    
    def get(self):
        pageArgs = PostFilter().loadMainPage("gen_page", self.request.get("pg"))
        pageArgs['currpage'] = "/general"
        self.render_template('index.html', pageArgs)

class DietPage(BaseHandler):
    
    def get(self):
        pageArgs = PostFilter().loadMainPage("de_page", self.request.get("pg"))
        pageArgs['currpage'] = "/diet_and_excercise"
        self.render_template('index.html', pageArgs)

class ProfilePage(BaseHandler):
    
    def get(self):
        if users.get_current_user():
            pf = PostFilter()
            self.render_template('profile.html', {'pagesize' : PostFilter.page_size, 
                                                  "totalposts" : pf.totalPosts(), "default" : PostFilter.mainarea, 'currpage' : '/profile'})
        else:
            message= "You must login to access this page".encode("utf8")
            self.redirect('/logout?message=' + message)

    def post(self):
        if users.get_current_user():
            error_str = None
            max_page = str(self.request.get("max"))
            mainpage = self.request.get("radio")
            pf = PostFilter()
            if max_page and max_page.isdigit():
                pf.setPagesize(pf, int(max_page))
                pf.setMainarea(pf, mainpage)
            else:
                error_str = "<p>That is not a valid number.</p>"
            self.render_template('profile.html', {'pagesize' : PostFilter.page_size, 
                                                  "totalposts" : pf.totalPosts(), 
                                                  "default" : PostFilter.mainarea, 
                                                  'currpage' : '/profile', 'error' : error_str})
        else:
            message= "You must login to access this page".encode("utf8")
            self.redirect('/logout?message=' + message)
            
class AboutPage(BaseHandler):
    def get(self):
        self.render_template('about.html', {'currpage' : '/about' })

class ContactPage(BaseHandler):
    def get(self):
        self.render_template('contact.html', {'currpage' : '/contact' })

class PostHandler(BaseHandler, blobstore_handlers.BlobstoreUploadHandler):
    
    def setPageTags(self, post):
        notEmpty = False
        if self.request.get('esl'):
            post.esl_page = True
            notEmpty = True
        else:
            post.esl_page = False
        if self.request.get('gen'):
            post.gen_page = True
            notEmpty = True
        else:
            post.gen_page = False
        if self.request.get('life'):
            post.life_page = True
            notEmpty = True
        else:
            post.life_page = False
        if self.request.get('de'):
            post.de_page = True
            notEmpty = True
        else:
            post.de_page = False
        if self.request.get('phil'):
            post.phil_page = True
            notEmpty = True
        else:
            post.phil_page = False
        return notEmpty

    def post(self):
        if users.get_current_user():
            error_str = ""
            #checking upload size
            upload_files = self.get_uploads('file')
            if upload_files.__sizeof__() > blobstore.MAX_BLOB_FETCH_SIZE:
                upload_files = None
                error_str = error_str + "<p>Picture size is too large.</p>" 
                
            if upload_files:  
                blob_info = upload_files[0]
                blob_key = blob_info.key()
            else:
                blob_key = None 
        
            post_sub = self.request.get('subject')
            post_content = self.request.get('content')
            if self.request.get('video'): 
                if MediaHelper().validate_vid_url(self.request.get('video')):
                    vid_url = self.request.get('video')
                else: 
                    vid_url = None
                    error_str = error_str + "<p>The youtube url you entered is invalid.</p>"
            else:
                vid_url = None
                
            date_str = self.request.get('date')
        
            #make datetime
            if not date_str == None:
                date = datetime.strptime(date_str,'%m/%d/%Y')
                time = datetime.time(datetime.now())
                dt = datetime.combine(date, time)
            else:
                dt = None
                
            is_post = self.request.get('post', None)

            post_stat = ""
            if is_post:
                post_stat = "Published"
            else:
                post_stat = "Saved"
        
            #save/update post
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
        
            if not self.setPageTags(post) and is_post:
                error_str = error_str + "<p>Select at least one publish area.</p>" 
                
            #save is error    
            if error_str:
                post.status = "Saved"
                
            post.put()
            if error_str:
                self.redirect('/post?post_id=' + str(post.key()) + "&error=" + error_str)
            elif is_post:
                self.redirect('/')
            else:
                self.redirect('/post?post_id=' + str(post.key()))
        else:
            message= "You must login to access this page".encode("utf8")
            self.redirect('/logout?message=' + message)
        

    def get(self):
        if users.get_current_user():
            upload = blobstore.create_upload_url('/post')
            if self.request.GET.get('post_id', None):
                key = self.request.get('post_id')
                error_str = self.request.get('error') 
                post = db.get(key)
                text = post.text
                title = post.title
                youtube = post.video_url
                image = MediaHelper().getImageURL(post.blob_key)
                date = post.date.strftime('%m/%d/%Y')
                self.render_template('post.html', {'text' : text, 'title' : title, 'id' : key, 
                                                   'upload_url' : upload, 'date' : date, 
                                                   'youtube' : youtube, 'image' : image, 
                                                   'fulldate' : post.date, 'esl' : post.esl_page,
                                                   'gen' : post.gen_page, 'life' : post.life_page,
                                                   'de' : post.de_page, 'phil' : post.phil_page, 
                                                   'currpage' : '/post', 'error' : error_str})
            else:   
                self.render_template('post.html', {'upload_url' : upload, 'currpage' : '/post' })
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
        self.render_template('logout.html', {'message' : message, 'users' : users, 'currpage' : '/logout' })
                    
            
class DeletePost(BaseHandler):
    
    def post(self):
        if users.get_current_user():
            post = db.get(self.request.get("post_id"))
            page = self.request.get("current_page")
            if post.blob_key:
                blobstore.delete_async(post.blob_key.key())
            post.delete()
            self.redirect(page)
        else:
            url = users.CreateLogoutURL('/logout?message=' + self.message, _auth_domain=None)
            self.redirect(url)

class DeleteImage(BaseHandler):
    
    def post(self):
        if users.get_current_user():
            post_id = self.request.get("post_id")
            post = db.get(post_id)
            if post.blob_key:
                blobstore.delete_async(post.blob_key.key())
                post.blob_key=None
                post.put()
        else:
            url = users.CreateLogoutURL('/logout?message=' + self.message, _auth_domain=None)
            self.redirect(url)


        
