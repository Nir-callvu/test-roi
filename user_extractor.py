# -------------------------------------------------------------------------------
# user_extractor
# -------------------------------------------------------------------------------
# A class to extract jobs from the DB
#-------------------------------------------------------------------------
# Author:       Gladiators
# Last updated: Dec 2015
#-------------------------------------------------------------------------

import logging
import db_handler
import user
import webapp2
import os
import jinja2
import logins
from google.appengine.api import users

jinja_environment = jinja2.Environment(    loader=
                                        jinja2.FileSystemLoader(os.path.dirname(__file__)))
                                        

class userfinder():
    def __init__(self):
        logging.info('Initializing userfinder')
        self.m_DbHandler=db_handler.DbHandler()

        self.m_NumberOfRows=0
    

#gets one user from the db and returns as the only item in a list!
    def get_one_user(self, email):
        logging.info('In userfinder.get_one_user')
        self.m_DbHandler.connectToDb()
        cursor=self.m_DbHandler.getCursor()
        sql =     """
                SELECT nickname, python, statistics, java, r, sql_skill, databases_skill, presentation, dataanalysis, finance, marketing, leadership  
                FROM team19.users
                WHERE email=%s
                """
        cursor.execute(sql, (email,))
        self.m_NumberOfRows = int(cursor.rowcount)
        logging.info("fetching user: "+ str(email))
        record=cursor.fetchone()
        logging.info('finished fetching from the db, now setting up the user')
        logging.info('the user details:     ' +str(record))
      
      #a condition for logins.cheat_login        
        if record == None or len(record) == 0:
            return None
        else:
            only_user=user.user()        
            only_user.email = email
            only_user.nickname = record[0]
            only_user.python = record[1]
            only_user.statistics = record[2]
            only_user.java = record[3]
            only_user.r = record[4]
            only_user.sql_skill = record[5]
            only_user.databases_skill = record[6]
            only_user.presentation = record[7]
            only_user.dataanalysis = record[8]
            only_user.finance = record[9]
            only_user.marketing = record[10]
            only_user.leadership = record[11]
        
            return only_user
  
	
#update skills for a user
class update_user(webapp2.RequestHandler):
# register a new user - first save his credentials in the db, then make him login with google account
    def get(self):
        logging.info('in: update_user.post')
        #check if user logged in!
        if not logins.showStatus():
            self.redirect('/login')
        #get the credentials of the connected user
        logging.info('user logged in')
        current_user = userfinder()
        user_to_update = user.user()
        user_to_update = current_user.get_one_user(users.get_current_user().email())
        #send to update_user with parameters of the user
        template = jinja_environment.get_template('update_user.html') 
        parameters_for_template = {	'user_to_update': user_to_update }
        self.response.write(template.render(parameters_for_template))

           
  
  