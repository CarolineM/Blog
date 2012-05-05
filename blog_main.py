import webapp2
from google.appengine.ext.webapp.util import run_wsgi_app
from views import MainPage, CreatePost, DeletePost, EditPost


application = webapp2.WSGIApplication([
        ('/', MainPage), 
        ('/newpost', CreatePost), 
        ('/edit/([\d]+)', EditPost),
        ('/delete/([\d]+)', DeletePost)
        ],
        debug=True)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
