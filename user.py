# -------------------------------------------------------------------------------
# user
# -------------------------------------------------------------------------------
# A class to manage the users + create (and save to DB)
#-------------------------------------------------------------------------
# Author:       Gladiators
# Last updated: Dec 2015
#-------------------------------------------------------------------------

import logging
import db_handler

class user():
    def __init__(self):
        logging.info('Initializing user')
        self.m_DbHandler=db_handler.DbHandler()

        # create data members of the class user
        self.email = ""
        self.nickname = ""
        self.gender = ""
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
        
        
        self.rec_bol = bool

    def saveToDb(self):
        logging.info('In user.saveToDb')
        self.m_DbHandler.connectToDb()
        cursor=self.m_DbHandler.getCursor()
        sql =     """
                INSERT INTO team19.users(email,nickname, gender, python, statistics, java, r, sql_skill, databases_skill, presentation, dataanalysis, finance, marketing, leadership) 
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """
        cursor.execute( sql, 
                        (self.email, self.nickname, self.gender, self.python,self.statistics,self.java,self.r,self.sql_skill,self.databases_skill,self.presentation,self.dataanalysis,self.finance,self.marketing,self.leadership))
        self.m_DbHandler.commit()
        logging.info('user created:  '+ str(self.email))
        return


    def update_in_Db(self, user_email):
        logging.info('In user.update_in_Db')
        self.m_DbHandler.connectToDb()
        cursor=self.m_DbHandler.getCursor()
        sql =     """
                UPDATE users
                SET python=%s, statistics=%s, java=%s, r=%s, sql_skill=%s, databases_skill=%s, presentation=%s, dataanalysis=%s, finance=%s, marketing=%s, leadership=%s) 
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                WHERE email=%s
                """
        cursor.execute( sql, 
                        (self.python,self.statistics,self.java,self.r,self.sql_skill,self.databases_skill,self.presentation,self.dataanalysis,self.finance,self.marketing,self.leadership,self.email))
        self.m_DbHandler.commit()
        logging.info('user updated:  '+ str(self.email))
        return
        
