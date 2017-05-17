# -------------------------------------------------------------------------------
# b_companies
# -------------------------------------------------------------------------------
# A class to manage the companies create (and save to DB)
#-------------------------------------------------------------------------
# Author:       Gladiators
# Last updated: Dec 2015
#-------------------------------------------------------------------------

import logging
import db_handler

class company():
    def __init__(self):
        logging.info('Initializing company')
        self.m_DbHandler=db_handler.DbHandler()

        # create data members of the class company
        self.brand = ""
        self.description = ""
        self.recruiter = ""


    def saveToDb(self, rec_mail):
        logging.info('In company.saveToDb')
        self.m_DbHandler.connectToDb()
        cursor = self.m_DbHandler.getCursor()
        sql =     """
                INSERT INTO team19.companies(brand,description, recruiter)
                VALUES(%s,%s,%s)
                """
        cursor.execute(sql,
                        (self.brand, self.description, rec_mail))
        self.m_DbHandler.commit()
        logging.info('company created:  '+ str(self.brand))
        return

