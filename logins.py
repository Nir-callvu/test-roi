# ------------------------------------------------------
# login classes - register, login and logout
# ------------------------------------------------------

# ------------------------------------------------------
# Author       - Gladiators
# Last updated - Dec 2015                                
# ------------------------------------------------------


import webapp2
from google.appengine.api import users
import logging
import user_extractor
import jinja2
import os

jinja_environment = jinja2.Environment(    loader=
                                        jinja2.FileSystemLoader(os.path.dirname(__file__)))
                                        

class login(webapp2.RequestHandler):
#login user - with google account
    def get(self):
        logging.info('In Login.get')
        logged_user = users.get_current_user()  
        # if the user object exists (the user is logged in to google)
        if logged_user:
            logging.info('The user is logged in')
            self.redirect('/browse_jobs')
        # The user object doesn't exist ( the user is not logged to google)
        else:      
            logging.info('The user object does not exist')
            self.redirect(users.create_login_url('/cheat_login'))


  
class user_registration(webapp2.RequestHandler):
#registration - after login with google
    def get(self):
        logging.info('In user_registration')
        logged_user = users.get_current_user()  
        # if the user object exists (the user is logged in to google)
        if logged_user:
            logging.info('The user is logged in')
            template = jinja_environment.get_template('register.html') 
            parameters_for_template = {    'is_logged' : logged_user}
            self.response.write(template.render(parameters_for_template)) 
        # The user object doesn't exist ( the user is not logged to google)
        else:      
            logging.info('The user is not logged in! ')
            self.redirect(users.create_login_url('/user_registration'))
  
        
#logout and back to main_page
class logout(webapp2.RequestHandler):
    def get(self):
        logging.info('In Logout.get')
        # if the user is logged in - we will perform log out
        logged_user = users.get_current_user()
        if logged_user:
            logging.info('The user is logged in - performing logout ')
            self.redirect(users.create_logout_url('/main_page'))

        else:
            logging.info('user is now not logged in ')
            self.redirect('/main_page')


class showStatus(webapp2.RequestHandler):
    def get(self):
        logging.info('In ShowStatus')      
        logged_user = users.get_current_user()
        if logged_user:
            logging.info('The user is logged in to google')
            return True
        else:
            logging.info('not logged in')  
            return False

            