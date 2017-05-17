# -------------------------------------------------------------------------------
# jc_creator
# -------------------------------------------------------------------------------
# A class to extract jobs from the DB
#-------------------------------------------------------------------------
# Author:       Gladiators
# Last updated: Dec 2015
#-------------------------------------------------------------------------
import logging
import company_extractor
import jinja2
import os
import user
import db_handler
from google.appengine.api import users
import webapp2

jinja_environment = jinja2.Environment(    loader=
                                        jinja2.FileSystemLoader(os.path.dirname(__file__)))


#a class to ceate a company and save it in the DB, gets the parameters from add_company
class create_company(webapp2.RequestHandler):
    def get(self):
        logging.info('create_company - check if user logged on')
        recruiter = user.user()       
        recruiter = users.get_current_user()
        if not recruiter:
            self.redirect('/user_login')  
        else:
            logging.info('seding to add_company.html')
            #send to add_company for post method
            template = jinja_environment.get_template('add_company.html') 
            parameters_for_template = { 'is_logged' : recruiter.nickname()}
            self.response.write(template.render(parameters_for_template)) 
        

        
class create_job(webapp2.RequestHandler):
    def get(self):
        recruiter = user.user()       
        recruiter = users.get_current_user()
        logging.info('in jc_creator.create_job - check if user logged on  ')
        if not recruiter:
            self.redirect('/user_login')
        else:
            logging.info('in jc_creator.create_job - user logged on, check if he opened a company before')            
            recruiter_email = (users.get_current_user()).email()       
        #check if the user is a recruiter, meaning he added a company
            companies_from_db = company_extractor.company_finder()
            companies_to_show = companies_from_db.get_rec_companies(recruiter_email)   
            if len(companies_to_show) == 0:
                logging.info('The user is not a recruiter, he did not add any company!')
                self.redirect('/add_company')                     
        #send to new_job_form for post method 
            logging.info('seding to new_job_form.html')
            parameters_for_template = { 'list_of_comp': companies_to_show,
                                        'is_logged' : recruiter.nickname()}    
            template = jinja_environment.get_template('new_job_form.html') 
            self.response.write(template.render(parameters_for_template))

def highest_job_num():
    logging.info('in jc_creator.highest_job_num   ')
    Handler = db_handler.DbHandler()
    Handler.connectToDb()
    cursor = Handler.getCursor()
    sql =     """
                SELECT max(job_num)                
                FROM jobs
            """
    cursor.execute(sql)                
    highest = cursor.fetchone()
    highest_num = int(highest[0])
    logging.info('highest job_num:     '  + str(highest))
    return highest_num
        

        
        




