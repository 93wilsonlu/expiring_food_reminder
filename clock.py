from apscheduler.schedulers.blocking import BlockingScheduler
import requests
import os

sched = BlockingScheduler()


@sched.scheduled_job('cron', day_of_week='mon-sun', hour=8)
def scheduled_job():
    requests.post('https://expiring-food-linebot.herokuapp.com/daily_work',
                  data={'password': os.environ.get('DAILY_WORK_PASSWORD')})


sched.start()