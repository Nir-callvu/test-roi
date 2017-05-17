# ------------------------------------------------------
# Send Mail with Database
# ------------------------------------------------------
# ------------------------------------------------------
# Author       - Gladiators
# Last updated - Dec 2015                                
# ------------------------------------------------------

import webapp2
import jinja2
import os
import db_handler
from google.appengine.api import users
#custom modules
import logging
import job
import jobs_extractor
import nominee
import nominee_extractor
import records_jb_recruiter
import records_jb_recruiter_extractor
import logins
import company
import company_extractor
import user
import user_extractor
import jc_creator



jinja_environment = jinja2.Environment(    loader=
                                        jinja2.FileSystemLoader(os.path.dirname(__file__)))

# -------------------------------------------------------------
# main page of the app
class main_page(webapp2.RequestHandler):
    def get(self):
        logging.info('main_page')        
          #diaplay the entry page
        #first check if the user is logged in
        is_logged = users.get_current_user()      
        if is_logged:
            login_to_html = is_logged.nickname()
        else:
            login_to_html = False 
        logging.info(str(login_to_html))     
        template = jinja_environment.get_template('main_page.html') 
        parameters_for_template = {    'is_logged' : login_to_html}
        self.response.write(template.render(parameters_for_template))        


# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# classes for different views for the user:    

class browse_jobs(webapp2.RequestHandler):
    def get(self):

        logging.info('browse_jobs.get()')
        all_jobs=jobs_extractor.jobfinder()
        retrieved_jobs=all_jobs.getalljobs()
        logging.info('retrieved all the jobs in the db' )
        
            #get a list of all the recruiters to allow filtering by recruiter
        recruiters=records_jb_recruiter_extractor.jbr_finder()
        list_of_rec = recruiters.getallrecruiters()
        
        is_logged = users.get_current_user()
        #check if the user is logged in to calculate suitability        
        if is_logged:
            jobs_to_show = retrieved_jobs.calc_jobs(is_logged.email())
            login_to_html = is_logged.nickname()
        else:
            jobs_to_show = retrieved_jobs.display_jobs()
            login_to_html = False

        #Display the jobs using jinja2
        logging.info('the jobs to show:    ' + str(jobs_to_show))        
        parameters_for_template = {'list_of_jobs' : jobs_to_show,
                                    'len_of_list' : len(jobs_to_show),                                  
                                   'is_logged' : login_to_html,
                                   'list_of_rec' : list_of_rec}
        my_template = jinja_environment.get_template('browse_all_jobs.html') #new HTML
        self.response.out.write(my_template.render(parameters_for_template))        


#browse by recruiter == by company, show all jobs by certian recruiter
class browse_jb_recruiter(webapp2.RequestHandler):
    def post(self):
        logging.info('browse_jb_recruiter.get()')
        recruiter_email = self.request.get('chosen_rec')
        jobs_finder = records_jb_recruiter_extractor.jbr_finder()  
        job_nums_by_rec = jobs_finder.getalljobs(recruiter_email)  #tuple that is a list of jobs by the single recruiter
        #retrieve titles and number of nominees for each job number
        lst_of_jobs = jobs_extractor.jobfinder()      
        jobs_by_rec = lst_of_jobs.get_jb_lst(job_nums_by_rec)  #list of jobs (job_num, title, company)
        jobs_to_show = nominee_extractor.get_noms_for_job(jobs_by_rec)            
        
        #check if user logged in for the online display 
        is_logged = users.get_current_user()       
        if is_logged:
            login_to_html = is_logged.nickname()
        else:
            login_to_html = False           
        template = jinja_environment.get_template('show_jobs_by_rec.html')
        parameters_for_template = {    'list_of_jobs' : jobs_to_show, 'is_logged' : login_to_html,
                                        'recruiter' : recruiter_email }
        self.response.write(template.render(parameters_for_template))        

#show list of nominees that applied for a job
class browse_nominees(webapp2.RequestHandler):
    def post(self):
        logging.info('shownominees.get()')
        #check if user logged in for the online display 
        is_logged = users.get_current_user() 
        if is_logged:
            login_to_html = is_logged.nickname()
        else:
            login_to_html = False         
        job_num = self.request.get('job_num')
        #get all the nominees for the job:
        all_nominees = nominee_extractor.nominees_finder() 
        nominee_lst = all_nominees.getallnoms(job_num)  #a nominees_finder instance list of users applied for the job
        if len(nominee_lst.allnoms) == 0 :
            noms_to_display = []
            num_of_noms = 0
        else: 
            noms_to_display= nominee_lst.calc_nominees(job_num)  #returns a sorted list by suitability
            num_of_noms = len(noms_to_display)
        logging.info('list of nominees:      ' +str(noms_to_display))
        template = jinja_environment.get_template('show_nominees_by_job.html') #different html according to demands
        parameters_for_template = {    'list_of_nominees': noms_to_display,
                                     'is_logged' : login_to_html,
                                     'num_of_noms' : num_of_noms}
        self.response.write(template.render(parameters_for_template))        


class show_personal_info(webapp2.RequestHandler):
    def get(self):
        logging.info('show_personal_info.get')
        #check if user logged in for the online display 
        is_logged = users.get_current_user()       
        if is_logged:                  
            #the user is logged on:
            login_to_html = is_logged.nickname()
            user_to_show = is_logged.email()    
            job_nums = nominee_extractor.get_jobs_for_user(user_to_show)   #a tuple with all the user jobs
            jobs_applied = jobs_extractor.jobfinder()      
            jobs_to_show = jobs_applied.get_jb_lst(job_nums)        
            # send all to jinja    
            template = jinja_environment.get_template('personal_info.html')
            parameters_for_template = {    'list_of_jobs': jobs_to_show, 'is_logged' : login_to_html }
            self.response.write(template.render(parameters_for_template))    
        else:   
              #the user is not logged on
          self.redirect('/user_login')
        
 
class leave_feedback(webapp2.RequestHandler):
    def get(self):
        logging.info('leave_feedback') 
        #first check if the user is logged in
        is_logged = users.get_current_user()      
        if is_logged:
            login_to_html = is_logged.nickname()
        else:
            login_to_html = False 
        logging.info(str(login_to_html))     
        template = jinja_environment.get_template('leave_feedback.html') 
        parameters_for_template = {    'is_logged' : login_to_html}
        self.response.write(template.render(parameters_for_template))   
        
class save_feedback(webapp2.RequestHandler):
    def post(self):
        logging.info('in: save_feedback') 
        f_name = self.request.get('f_name')
        f_content = self.request.get('f_content')
        Handler = db_handler.DbHandler()        
        Handler.connectToDb()
        cursor=Handler.getCursor()
        sql =     """
                INSERT INTO team19.feedback(name,content)
                VALUES(%s,%s)
                """
        cursor.execute( sql, (str(f_name),str(f_content),))
        Handler.commit()
        logging.info('feedback saved to DB! ')
        self.redirect('/main_page')

 
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# classes for the creation of all the entities:        

class create_company_in_db(webapp2.RequestHandler):
    def post(self):
        logging.info('in: create_company_in_db')
      #  recruiter = user.user()       
        recruiter_email = (users.get_current_user()).email()
        new_comp=company.company()
        new_comp.brand = self.request.get('new_company_name')
        new_comp.description = self.request.get('new_company_description')
        new_comp.saveToDb(recruiter_email)
        self.redirect('/create_job')

class create_nominee(webapp2.RequestHandler):
    def post(self):
        logging.info('in: add_nominee')
      #  recruiter = user.user()       
        new_record=nominee.nominee()
        new_record.email = (users.get_current_user()).email()
        new_record.job_num = self.request.get('job_to_apply')
        new_record.saveToDb()
        self.redirect('/browse_all_jobs')
        
class remove_nominee(webapp2.RequestHandler):
    def post(self):
        logging.info('in: remove_nominee ')
      #  recruiter = user.user()       
        record_to_remove=nominee.nominee()
        record_to_remove.email = (users.get_current_user()).email()
        record_to_remove.job_num = self.request.get('job_to_remove')
        for_log = (record_to_remove.job_num,record_to_remove.email)
        logging.info('job num to remove:      ' +str(for_log))
        record_to_remove.erasefromDb()
        self.redirect('/personal_info')
 
 
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# classes for the user registration process 

#a class for unregistered users logging in - check if they are registered
class cheat_login(webapp2.RequestHandler):
    def get(self):
        logging.info('In cheat_login')
        logged_user = users.get_current_user()         
        current = user_extractor.userfinder()
        in_db = current.get_one_user(logged_user.email())
        if in_db == None:
            self.redirect('/user_registration')
        else:
            self.redirect('/main_page')

 
class register_in_db(webapp2.RequestHandler):
# register a new user - first save his credentials in the db, then make him login with google account
    def post(self):
        logging.info('in: register')
        #first login with google!!
        g_user = users.get_current_user() 
        if not g_user:   
            logging.info('The g_user object does not exist')
            self.redirect(users.create_login_url('/register')) 
        new_user = user.user()
        #Request data from the POST request
        new_user.email = g_user.email()
        new_user.nickname = self.request.get('new_user_nickname')
        new_user.gender = self.request.get('new_user_gender')
        new_user.python = self.request.get('new_user_python')
        new_user.statistics = self.request.get('new_user_statistics')
        new_user.java = self.request.get('new_user_java')
        new_user.r = self.request.get('new_user_r')
        new_user.sql_skill = self.request.get('new_user_sql_skill')
        new_user.databases_skill = self.request.get('new_user_databases_skill')
        new_user.presentation = self.request.get('new_user_presentation')
        new_user.dataanalysis = self.request.get('new_user_dataanalysis')
        new_user.finance = self.request.get('new_user_finance')
        new_user.marketing = self.request.get('new_user_marketing')
        new_user.leadership = self.request.get('new_user_leadership')       
        new_user.saveToDb() # add new_user to the db
        logging.info('saved:' + new_user.email + 'in the db')
        #redirect the user to browse_jobs
        self.redirect('/browse_all_jobs')
    

#update user in the db - comes from update_user.html        
class update_user_in_db(webapp2.RequestHandler):
# update the user in the db
    def post(self):                
        logging.info('in: update_user_in_db')       
        current_user = user.user()
        #Request data from the POST request
        current_user.email = (users.get_current_user()).email()
        current_user.python = self.request.get('user_to_update_python')
        current_user.statistics = self.request.get('user_to_update_statistics')
        current_user.java = self.request.get('user_to_update_java')
        current_user.r = self.request.get('user_to_update_r')
        current_user.sql_skill = self.request.get('user_to_update_sql_skill')
        current_user.databases_skill = self.request.get('user_to_update_databases_skill')
        current_user.presentation = self.request.get('user_to_update_presentation')
        current_user.dataanalysis = self.request.get('user_to_update_dataanalysis')
        current_user.finance = self.request.get('user_to_update_finance')
        current_user.marketing = self.request.get('user_to_update_marketing')
        current_user.leadership = self.request.get('user_to_update_leadership')       
        #save in DB
        current_user.update_in_Db(current_user.email) # add new_user to the db
        logging.info('updated:' + current_user.email + 'in the db')    
        #redirect the user to browse_jobs
        self.redirect('/browse_all_jobs')        
 



   
# create a new job
class create_job_in_db(webapp2.RequestHandler):

    def post(self):
        logging.info('create_job_in_db')
        new_job=job.job()
        #Request data from the POST request
        new_job.job_title = self.request.get('new_job_title')
        new_job.company = self.request.get('chosen_company')
        new_job.python = self.request.get('new_job_python')
        new_job.statistics = self.request.get('new_job_statistics')
        new_job.java = self.request.get('new_job_java')
        new_job.r = self.request.get('new_job_r')
        new_job.sql_skill = self.request.get('new_job_sql')
        new_job.databases_skill = self.request.get('new_job_python')
        new_job.presentation = self.request.get('new_job_databases')
        new_job.dataanalysis = self.request.get('new_job_dataanalysis')
        new_job.finance = self.request.get('new_job_finance')
        new_job.marketing = self.request.get('new_job_marketing')
        new_job.leadership = self.request.get('new_job_leadership')
        
        #create a new following job number
        new_job.job_num = (jc_creator.highest_job_num())+1
        logging.info('new job num:    '  +str(new_job.job_num))        
        logging.info('create_job in jobs table')
        new_job.saveToDb()
  #initilize record before inserting to jobs_by_recruiter
        logging.info('create_job in jobs_by_recruiter table')
        new_jb_rec = records_jb_recruiter.job_by_rec()     
        new_jb_rec.job_num = new_job.job_num
        new_jb_rec.recruiter = (users.get_current_user()).email()
        # add new_jb_rec to the db (recruiter_jobs)
        new_jb_rec.saveToDb()        
        self.redirect('/main_page')
        
# -------------------------------------------------------------
# Routing
# -------------------------------------------------------------
app = webapp2.WSGIApplication([ ('/browse_all_jobs', browse_jobs),
                                ('/browse_jb_recruiter', browse_jb_recruiter),
                                ('/browse_nominees', browse_nominees),
								
				('/add_company', 'jc_creator.create_company'),
                ('/create_company_in_db', create_company_in_db),
                ('/create_job', 'jc_creator.create_job'),
                ('/create_job_in_db', create_job_in_db),

								('/create_nominee', create_nominee),
                                ('/remove_nominee', remove_nominee),
				
                ('/personal_info', show_personal_info),                             
				
                                ('/user_login', 'logins.login'), 
                                ('/cheat_login', cheat_login), 
                                ('/user_logout', logins.logout),
								
				('/user_registration', 'logins.user_registration'),                                
                ('/register_in_db', register_in_db),
                ('/update_user', 'user_extractor.update_user'),
                ('/update_user_in_db', update_user_in_db),
                  
								('/leave_feedback', leave_feedback),
								('/save_feedback', save_feedback),
								
                                ('/main_page', main_page),
                                ('/', main_page)
                                ],
                                debug=True)




                                