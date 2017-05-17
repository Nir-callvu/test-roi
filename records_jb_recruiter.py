# -------------------------------------------------------------------------------
# records_jb_recruiter
# -------------------------------------------------------------------------------
# A class to manage the jobs arranged by recruiter (different DB - indexes)
#-------------------------------------------------------------------------
# Author:       Gladiators
# Last updated: Dec 2015
#-------------------------------------------------------------------------

import logging
import db_handler

class job_by_rec():
    def __init__(self):
        logging.info('Initializing job_by_rec')
        self.m_DbHandler=db_handler.DbHandler()

        # create data members of the class job_by_rec
        self.recruiter = ""
        self.job_num = ""
        self.post_date = ""

    def saveToDb(self):
        logging.info('In job.saveToDb - by rec')
        self.m_DbHandler.connectToDb()
        cursor=self.m_DbHandler.getCursor()
        sql =     """
                INSERT INTO team19.jobs_by_recruiter(recruiter,job_num,post_date) 
                VALUES(%s,%s,sysdate())
                """
        cursor.execute( sql, 
                        (self.recruiter,self.job_num))
#need this?        self.job_num = cursor.lastrowid    
        self.m_DbHandler.commit()
        logging.info('job_by_rec created a new record:  '+ str(self.job_num))
        return

    def getContentInHtmlFormat(self):
        return self.m_Content.replace("\r\n", "<br />")
                                      
           
           
           