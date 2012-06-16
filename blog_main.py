import webapp2
from google.appengine.ext.webapp.util import run_wsgi_app
from views import MainPage, PostHandler, DeletePost


application = webapp2.WSGIApplication([
        ('/', MainPage), 
        ('/post', PostHandler), 
        ('/delete/([\d]+)', DeletePost)
        ],
        debug=True)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
