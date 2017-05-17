# -------------------------------------------------------------------------------
# calc_suit - calculate suitability
# -------------------------------------------------------------------------------
# A class to manage the users + create (and save to DB)
#-------------------------------------------------------------------------
# Author:       Gladiators
# Last updated: Dec 2015
#-------------------------------------------------------------------------
import logging
#import user
#import job


 #a function to calculate suitability between a user and a job 
def calc_suit(user, job):
        logging.info('in calc_suit')
        logging.info('convert reqs to 2 lists')
        user_skills = []
        user_skills.append(int(user.python))
        user_skills.append(int(user.statistics))
        user_skills.append(int(user.java))
        user_skills.append(int(user.r))
        user_skills.append(int(user.sql_skill))
        user_skills.append(int(user.databases_skill))
        user_skills.append(int(user.presentation))
        user_skills.append(int(user.dataanalysis))
        user_skills.append(int(user.finance))
        user_skills.append(int(user.marketing))
        user_skills.append(int(user.leadership))

        job_skills = []
        job_skills.append(int(job.python))
        job_skills.append(int(job.statistics))
        job_skills.append(int(job.java))
        job_skills.append(int(job.r))
        job_skills.append(int(job.sql_skill))
        job_skills.append(int(job.databases_skill))
        job_skills.append(int(job.presentation))
        job_skills.append(int(job.dataanalysis))
        job_skills.append(int(job.finance))
        job_skills.append(int(job.marketing))
        job_skills.append(int(job.leadership))       
        
        if len(user_skills) != len(job_skills):
            raise ValueError ('something is wrong with the application!!')

        logging.info('calculate')
        suitable = []
        for i in range(len(user_skills)):
                if job_skills[i]!=0:
                    if user_skills[i]>job_skills[i]:
                        suitable.append(100)
                    if job_skills[i]>=user_skills[i]:   
                        suitable.append(float(user_skills[i])/float(job_skills[i])*100)
        sum_score=sum(suitable)
        num_of_skills=len(suitable)
        if num_of_skills ==0:
            score = 0
        else: 
            score=float(sum_score)/float(num_of_skills)
        logging.info('score is:      ' +str(score))
        return int(score)  



