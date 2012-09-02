import webapp2
from google.appengine.ext.webapp.util import run_wsgi_app
from views import MainPage, PostHandler, SignInHandler, UserCheckerHandler, DeletePost, LogoutHandler, DeleteImage


application = webapp2.WSGIApplication([
        ('/', MainPage), 
        ('/post', PostHandler),
        ('/signin', SignInHandler),
        ('/userchecker', UserCheckerHandler),
        ('/logout', LogoutHandler),
        ('/delete', DeletePost),
        ('/delete_image', DeleteImage)
        ],
        debug=True)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
