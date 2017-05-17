# -------------------------------------------------------------------------------
# jobs_extractor
# -------------------------------------------------------------------------------
# A class to extract jobs from the DB
#-------------------------------------------------------------------------
# Author:       Gladiators
# Last updated: Dec 2015
#-------------------------------------------------------------------------

import logging
import db_handler
import job
import user_extractor
import user
import nominee_extractor
import calc_suit

class jobfinder():
    def __init__(self):
        logging.info('Initializing jobfinder')
        self.m_DbHandler=db_handler.DbHandler()

        # create data members of the class jobfinder
        self.m_NumberOfRows=0
        self.alljobs=[]
    
#returns all the jobs from the db
    def getalljobs(self):
        logging.info('In jobfinder.getalljobs')
        self.m_DbHandler.connectToDb()
        cursor=self.m_DbHandler.getCursor()
        sql =     """
                SELECT job_num,python,statistics,java,r,sql_skill,databases_skill,presentation,dataanalysis,finance,marketing,leadership,job_title,company
                FROM team19.jobs
                """
        cursor.execute(sql,)
        self.m_NumberOfRows = int(cursor.rowcount)
        logging.info("Number of records "+ str(self.m_NumberOfRows))
        job_records=cursor.fetchall()
        self.alljobs=[]
        logging.info('record - now is the problem??')
        for record in job_records:
            current_job=job.job()
            current_job.job_num=record[0]
            current_job.python = record[1]
            current_job.statistics = record[2]
            current_job.java = record[3]
            current_job.r = record[4]
            current_job.sql_skill = record[5]
            current_job.databases_skill = record[6]
            current_job.presentation = record[7]
            current_job.dataanalysis = record[8]
            current_job.finance = record[9]
            current_job.marketing = record[10]
            current_job.leadership = record[11]
            current_job.job_title = record[12]
            current_job.company = record[13]
            self.alljobs.append(current_job)
        return self

#get job nums, titles and companies job numbers
    def get_jb_lst(self, job_nums):
        logging.info('In jobfinder.get_jb_lst')
        self.m_DbHandler.connectToDb()
        self.alljobs = []
        #loop for retrieving the job titles from jobs table
        for i in range(len(job_nums)):           
            cursor=self.m_DbHandler.getCursor()
            sql =     """
                    SELECT job_title, company
                    FROM jobs
                    WHERE job_num=%s
                    """
            cursor.execute(sql, (job_nums[i][0],))
            job_titles=cursor.fetchone()
            logging.info('got from the DB:     ' + str(job_titles))			
            self.alljobs.append((job_nums[i], job_titles[0], job_titles[1]))
        logging.info('finished retrieving job titles and companies:      ' + str(self.alljobs)  + str(len(job_nums)))
	return self.alljobs  
		
	

#gets one job from the db and returns as the only item in a list!
    def get_one_job(self, job_num):
        logging.info('In jobfinder.get_one_job with job number:   ' +str(job_num))
        self.m_DbHandler.connectToDb()
        cursor=self.m_DbHandler.getCursor()
        sql =     """
                SELECT job_title, python, statistics, java, r, sql_skill, databases_skill, presentation, dataanalysis, finance, marketing, leadership
                FROM team19.jobs
                WHERE job_num=%s
                """
        cursor.execute(sql, (job_num,))  
        record=cursor.fetchone()
        logging.info('intilizing job:     ' +str(record))
        current_job=job.job()
        current_job.job_num=job_num
        current_job.job_title = record[0]
        current_job.python = record[1]
        current_job.statistics = record[2]
        current_job.java = record[3]
        current_job.r = record[4]
        current_job.sql_skill = record[5]
        current_job.databases_skill = record[6]
        current_job.presentation = record[7]        
        current_job.dataanalysis = record[8]
        current_job.finance = record[9]
        current_job.marketing = record[10]
        current_job.leadership = record[11]
        return current_job
  

    def display_jobs(self):
        logging.info('In jobs_extractor.display_jobs')        
            #build the complete list of tuples for display
        lst = []
        for i in range(len(self.alljobs)):
            lst.append((self.alljobs[i].job_num, self.alljobs[i].job_title, self.alljobs[i].company))
        return lst 

 
#gets a list of jobs and calculates suitability for each one - returns a list of tuples!!!
    def calc_jobs(self, user_email) :
        logging.info('In jobs_extractor.calc_jobs')        
        lst_one_user = user_extractor.userfinder()
        user_to_calc = user.user()
        user_to_calc = lst_one_user.get_one_user(user_email) #type user to compare the list of jobs with with 
             #add for each job a boolean parameter, if the user applied for the job
        user_jobs = nominee_extractor.get_jobs_for_user(user_email)
        applied_jobs = []  #list of boolean values of the jobs the user applied to from the general list
        for every_job in self.alljobs:
            if (every_job.job_num,) in user_jobs:
                applied_jobs.append(True)
            else:
                applied_jobs.append(False)               
        logging.info('user_jobs from nominee extractor:      ' + str(user_jobs) + '    ' +str(applied_jobs))  
            #build the complete list of tuples
        suit_list = []
        for i in range(len(self.alljobs)):
            suit_list.append((self.alljobs[i].job_num, self.alljobs[i].job_title, self.alljobs[i].company,
                              calc_suit.calc_suit(user_to_calc, self.alljobs[i]), applied_jobs[i]))
        lst = sorted(suit_list, key=lambda x: x[3])
        lst.reverse()
        
        return lst 
   
  
 

 