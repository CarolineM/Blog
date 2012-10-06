import webapp2
from google.appengine.ext.webapp.util import run_wsgi_app
from views import MainPage, PostHandler, SignInHandler, UserCheckerHandler, DeletePost, LogoutHandler, DeleteImage, SavedPage, ProfilePage, AboutPage, Upload 


application = webapp2.WSGIApplication([
        ('/', MainPage), 
        ('/post', PostHandler),
        ('/signin', SignInHandler),
        ('/userchecker', UserCheckerHandler),
        ('/logout', LogoutHandler),
        ('/delete', DeletePost),
        ('/delete_image', DeleteImage),
        ('/saved', SavedPage),
        ('/profile', ProfilePage),
        ('/about', AboutPage),
        ('/upload', Upload)
        ],
        debug=True)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
