from pytz import timezone

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor

from tasks import *

def init_scheduler(mongodb):
    jobstores = {
        'mongo': MongoDBJobStore(client=mongodb)
    }
    executors = {
        'default': ThreadPoolExecutor(20),
        'processpool': ProcessPoolExecutor(5)
    }
    job_defaults = {
        'coalesce': False,
        'max_instances': 3,
        'misfire_grace_time': 15*60,
    }
    scheduler = AsyncIOScheduler(job_defaults=job_defaults,timezone=timezone('UTC'))
    #scheduler.configure(jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone=utc)
    scheduler.start()
    return scheduler

def add_default_tasks(scheduler):
#    scheduler.add_job(reg_member, id='reg_member', trigger='cron', hours=22)
    scheduler.add_job(hello, id='hello', trigger='interval', seconds=15)
