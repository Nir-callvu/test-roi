# -------------------------------------------------------------------------------
# nominee_extractor
# -------------------------------------------------------------------------------
# A class to extract nominees by from the DB
#-------------------------------------------------------------------------
# Author:       Gladiators
# Last updated: Dec 2015
#-------------------------------------------------------------------------

import logging
import db_handler
import job
import jobs_extractor
import user
import user_extractor
import calc_suit
from google.appengine.api import users
import nominee

class nominees_finder():
    def __init__(self):
        logging.info('Initializing nominees_finder')
        self.m_DbHandler=db_handler.DbHandler()

        # create data members of the class jobfinder
        self.m_NumberOfRows=0
        self.allnoms=[]
    
#gets all the users that applied for the job
    def getallnoms(self, job_num):
        logging.info('In nominees_finder.getallnoms with job:    ' +str(job_num))
        self.m_DbHandler.connectToDb()
        cursor=self.m_DbHandler.getCursor()
        sql =     """
                SELECT user                
                FROM team19.nominees
                WHERE job_num = %s
                """
        cursor.execute(sql, (job_num,))                
        nom_records = cursor.fetchall()
        self.allnoms = []
        for record in nom_records:
            self.allnoms.append(record[0])
        logging.info('all the nominees found:      ' +str(nom_records))
        return self

                
#gets a list of users (emails) and calculates suitability for each one - returns nested list
    def calc_nominees(self, job_num) :
        logging.info('In calc_nominees with job: ' +str(job_num))
        lst_one_job = jobs_extractor.jobfinder()
        desired_job = job.job()
        
        desired_job = lst_one_job.get_one_job(job_num) #type job to compare the list of nominees with with
        suit_list = []
        for i in range(len(self.allnoms)):
            fetch_user = user_extractor.userfinder()
            user_to_compare = fetch_user.get_one_user(self.allnoms[i])
            logging.info('the desired job:    '   +str(desired_job.job_title)   + '    and the user to compare:   ' + str(user_to_compare.email))
            suit_list.append((self.allnoms[i], calc_suit.calc_suit(user_to_compare, desired_job)))
        lst = sorted(suit_list, key=lambda x: x[1])
        lst.reverse()
        return lst         
        
                
            #retrieves  number of nominees for a the list of job_numbers           
def get_noms_for_job(jobs):
    logging.info('In nominee_extractor.get_noms_for_job with jobs:   ' + str(jobs))
       #loop for retrieving the number of nominees from nominees table
    m_DbHandler=db_handler.DbHandler()
    job_list = []
    for one_job in jobs:
        cursor = m_DbHandler.getCursor()
        sql =     """
                    SELECT COUNT(user)                    
                    FROM team19.nominees
                    WHERE job_num=%s
                   """
        cursor.execute(sql,(one_job[0][0],))
        num_of_noms=cursor.fetchone()
     
        job_list.append([one_job[0], one_job[1], one_job[2], num_of_noms[0]])
        logging.info('finished retrieving job nominees')
    return job_list  
 

 #gets all the jobs the user applied for
def get_jobs_for_user(user_mail):
    logging.info('In nominee_extractor.get_jobs_for_user with user:   ' + str(user))
       #loop for retrieving the job_numbers from nominees table
    user_mail = users.get_current_user().email()
    m_DbHandler=db_handler.DbHandler()
    cursor = m_DbHandler.getCursor()
    sql =     """
                    SELECT job_num                    
                    FROM team19.nominees
                    WHERE user=%s
              """
    cursor.execute(sql, (user_mail,))  #should be user.email!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    jobs=cursor.fetchall()
    list_of_jobs = []
    for single_job in jobs:
        list_of_jobs.append(int(single_job[0]))
    logging.info('finished retrieving the jobs:         ' + str(jobs))
    return jobs   
 
 
 
 
 
 