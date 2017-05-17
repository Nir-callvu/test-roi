# -------------------------------------------------------------------------------
# job
# -------------------------------------------------------------------------------
# A class to manage the jobs create (and save to DB)
#-------------------------------------------------------------------------
# Author:       Gladiators
# Last updated: Dec 2015
#-------------------------------------------------------------------------

import logging
import db_handler

class job():
    def __init__(self):
        logging.info('Initializing job')
        self.m_DbHandler=db_handler.DbHandler()

        # create data members of the class job
        self.job_num = ""
        self.job_title = ""
        self.company = ""
        self.python = ""
        self.statistics = ""
        self.java = ""
        self.r = ""
        self.sql_skill = ""
        self.databases_skill = ""
        self.presentation = ""
        self.dataanalysis = ""
        self.finance = ""
        self.marketing = ""
        self.leadership = ""
        
         

    def saveToDb(self):
		logging.info('In job.saveToDb')
		self.m_DbHandler.connectToDb()
		cursor=self.m_DbHandler.getCursor()
		sql = 	"""
                INSERT INTO team19.jobs (job_num, job_title, company, python, statistics, java, r, sql_skill, databases_skill, presentation, dataanalysis, finance, marketing, leadership) 
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
				"""
		cursor.execute(sql, 
						(self.job_num,self.job_title,self.company,self.python,self.statistics,self.java,self.r,self.sql_skill,self.databases_skill,self.presentation,self.dataanalysis,self.finance,self.marketing,self.leadership,))
		self.m_DbHandler.commit()
		logging.info('job created is  '+ str(self.job_title))
		return


								  