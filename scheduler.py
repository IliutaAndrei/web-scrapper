from apscheduler.schedulers.blocking import BlockingScheduler
from main import run_scraper


scheduler = BlockingScheduler()

scheduler.add_job(run_scraper, 'cron', day_of_week="mon-sun", hour="12-18", minute=0)
scheduler.start()
