# -------------------------------------------------------------------------------
# company_extractor
# -------------------------------------------------------------------------------
# A class to extract all the companies from the DB
#-------------------------------------------------------------------------
# Author:       Gladiators
# Last updated: Dec 2015
#-------------------------------------------------------------------------

import logging
import db_handler
import company

class company_finder():
    def __init__(self):
        logging.info('Initializing company_finder')
        self.m_DbHandler=db_handler.DbHandler()

        # create data members of the class company_finder
        self.m_NumberOfRows=0
        self.allcompanies=[]
    
 
    def getallcompanies(self):
        logging.info('company_finder.getallcompanies')
        self.m_DbHandler.connectToDb()
        cursor=self.m_DbHandler.getCursor()
        sql =     """
                SELECT *                    
                FROM team19.companies
                """
        cursor.execute(sql)
        self.m_NumberOfRows = int(cursor.rowcount)
        logging.info("Number of companies "+ str(self.m_NumberOfRows))
        company_records=cursor.fetchall()
        self.allcompanies=[]
        logging.info('record - now is the problem?? allcompanies')
        for company in company_records:
            current_company=company.company()
            current_company.brand=record[0]
            current_company.description = record[1]
            current_company.recruiter = record[2]
            self.allcompanies.append(current_company)
        return self.allcompanies

#get companies formed by  a specific user
    def get_rec_companies(self, email):
        logging.info('company_finder.get_rec_companies')
        self.m_DbHandler.connectToDb()
        cursor=self.m_DbHandler.getCursor()
        sql =     """
                SELECT brand, description                    
                FROM team19.companies
                WHERE recruiter=%s
                """
        cursor.execute(sql, (email,))
        company_records=cursor.fetchall()
        self.allcompanies=[]
        logging.info('got all the companies added by the user:     ' +str(company_records))
        for record in company_records:
            current_company=company.company()
            current_company.brand=record[0]
            current_company.description = record[1]
            self.allcompanies.append(current_company)
        return self.allcompanies 
  
  
  