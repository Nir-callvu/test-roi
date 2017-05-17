# -------------------------------------------------------------------------------
# nominee
# -------------------------------------------------------------------------------
# A class to manage the users + create (and save to DB)
#-------------------------------------------------------------------------
# Author:       Gladiators
# Last updated: Dec 2015
#-------------------------------------------------------------------------

import logging
import db_handler

class nominee():
    def __init__(self):
        logging.info('Initializing nominee')
        self.m_DbHandler=db_handler.DbHandler()

        # create data members of the class nominee
        self.email = ""     #user applied email
        self.job_num = ""
        self.app_date = ""

    def saveToDb(self):
		logging.info('In nominee.saveToDb')
		self.m_DbHandler.connectToDb()
		cursor=self.m_DbHandler.getCursor()
		sql = 	"""
				INSERT INTO team19.nominees(job_num,user,app_date) 
				VALUES(%s,%s,sysdate())
				"""
		cursor.execute( sql, 
						(self.job_num,self.email))
  		self.m_DbHandler.commit()
		logging.info('nominee created is  '+ str(self.email))
		return

    def erasefromDb(self):
		logging.info('In nominee.earase from DB')
		self.m_DbHandler.connectToDb()
		cursor=self.m_DbHandler.getCursor()
		sql = 	"""
                DELETE FROM team19.nominees
                WHERE job_num=%s and user=%s

				"""
		cursor.execute( sql,(self.job_num[1:-2],self.email,))
  		self.m_DbHandler.commit()
		logging.info('nominee deleted is  '+ str(self.email) + '   from job:    ' + str(self.job_num))
		return		
		
									  