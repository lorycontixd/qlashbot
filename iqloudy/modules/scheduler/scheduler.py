from pytz import timezone

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from modules.scheduler import library as scheduler_library

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
    scheduler = AsyncIOScheduler(job_defaults=job_defaults,timezone=timezone('Europe/Rome'))
    #scheduler.configure(jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone=utc)
    scheduler.start()
    return scheduler

"""
Example scheduler trigers:
    scheduler.add_job(hello, id='hello-interval', args=['interval scheduling'], trigger='interval', seconds=5)
    scheduler.add_job(hello, id='hello-cron', args=['cron scheduling'], trigger='cron', second='5')
    scheduler.add_job(hello, id='hello-date', args=['date scheduling'], trigger='date')
"""
def add_default_tasks(scheduler):
    #scheduler.add_job(reg_member, id='reg_member', trigger='cron', hours=22)
    CEST = timezone('Europe/Rome')
    scheduler.add_job(scheduler_library.check_banlist_api, id='check_banlist_api', trigger='cron',hour='22', minute='0')
    scheduler.add_job(scheduler_library.hello_en,id="hello_en",trigger='cron',hour='10',minute='0')
    scheduler.add_job(scheduler_library.hello_it,id="hello_it",trigger='cron',hour='10',minute='0')
    scheduler.add_job(scheduler_library.reg_member,id='register-member',trigger='cron',hour='22',minute='0')
    scheduler.add_job(scheduler_library.giova,id="daily-saint",trigger='cron',hour='10',minute='0')
    scheduler.add_job(scheduler_library.invite_bot_ch,id='invite',trigger='cron',hour='13',minute='00')
    pass

def _get_jobs(scheduler):
    list = scheduler.get_jobs()
    return list
