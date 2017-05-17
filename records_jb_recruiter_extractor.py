# -------------------------------------------------------------------------------
# records_jb_recruiter_extractor
# -------------------------------------------------------------------------------
# A class to extract jobs by recruiter from the DB
#-------------------------------------------------------------------------
# Author:       Gladiators
# Last updated: Dec 2015
#-------------------------------------------------------------------------

import logging
import db_handler
import records_jb_recruiter

class jbr_finder():
    def __init__(self):
        logging.info('Initializing jbr_finder')
        self.m_DbHandler=db_handler.DbHandler()

        # create data members of the class jobfinder
        self.m_NumberOfRows=0
        self.alljobs=[]
    

    def getalljobs(self, rec_email):
        logging.info('records_jb_recruiter_extractor.getalljobs')
        self.m_DbHandler.connectToDb()
        cursor=self.m_DbHandler.getCursor()
        sql =     """
                SELECT job_num                    
                FROM team19.jobs_by_recruiter
                WHERE recruiter=%s
                """
        cursor.execute(sql, (rec_email,))
        job_records = cursor.fetchall()
        logging.info('jobs to find:   ' + str(job_records))
        self.alljobs=job_records
        return self.alljobs

    def getallrecruiters(self):
        logging.info('records_jb_recruiter_extractor.getallrecruiters')
        self.m_DbHandler.connectToDb()
        cursor=self.m_DbHandler.getCursor()
        sql =     """
                SELECT distinct(recruiter)
                FROM team19.jobs_by_recruiter
                """
        cursor.execute(sql)
        records = cursor.fetchall()
        recruiters=[]
        for record in records:
			recruiters.append(str(record[0]))
        logging.info(' recruiters:   ' + str(recruiters))
        return recruiters
  
  
  