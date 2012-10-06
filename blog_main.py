import webapp2
from google.appengine.ext.webapp.util import run_wsgi_app
import views 


application = webapp2.WSGIApplication([
        ('/', views.MainPage), 
        ('/post', views.PostHandler),
        ('/signin', views.SignInHandler),
        ('/userchecker', views.UserCheckerHandler),
        ('/logout', views.LogoutHandler),
        ('/delete', views.DeletePost),
        ('/delete_image', views.DeleteImage),
        ('/saved', views.SavedPage),
        ('/profile', views.ProfilePage),
        ('/about', views.AboutPage),
        ('/upload', views.Upload),
        ('/single', views.OnePost)
        ],
        debug=True)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
