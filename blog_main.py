import webapp2
from google.appengine.ext.webapp.util import run_wsgi_app
from views import MainPage, PostHandler, SignInHandler, UserCheckerHandler, DeletePost, LogoutHandler, DeleteImage, SavedPage, ESLPage, LifestylePage, PhilosophyPage, GeneralPage, ProfilePage, DietPage, AllPage, AboutPage, ContactPage 


application = webapp2.WSGIApplication([
        ('/', MainPage), 
        ('/post', PostHandler),
        ('/signin', SignInHandler),
        ('/userchecker', UserCheckerHandler),
        ('/logout', LogoutHandler),
        ('/delete', DeletePost),
        ('/delete_image', DeleteImage),
        ('/saved', SavedPage),
        ('/esl', ESLPage),
        ('/diet_and_exercise', DietPage),
        ('/lifestyle', LifestylePage),
        ('/philosophy', PhilosophyPage),
        ('/general', GeneralPage),
        ('/profile', ProfilePage),
        ('/all', AllPage),
        ('/about', AboutPage),
        ('/contact', ContactPage),
        ],
        debug=True)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
