"""myapp.py
Usage::
   (window1)$ python myapp.py worker -l info
   (window2)$ python
   # >>> from myapp import add
   # >>> add.delay(16, 16).get()
   32
You can also specify the app to use with the `celery` command,
using the `-A` / `--app` option::
    $ celery -A myapp worker -l info
With the `-A myproj` argument the program will search for an app
instance in the module ``myproj``.  You can also specify an explicit
name using the fully qualified form::
    $ celery -A myapp:app worker -l info
"""
from __future__ import absolute_import, unicode_literals

import requests
from celery import Celery
from celery.task import periodic_task
from datetime import timedelta

app = Celery(
    'myapp',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)

app.config_from_object('settings', namespace='CELERY')
# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.timezone = 'UTC'


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

@app.task(name='safetrees.my_address', bind=True)
          # unique name                # add self
def get_my_address(self):
    response = urllib.urlopen('http://httpbin.org/ip').read()
    parsed = json.loads(response)
    assert type(parsed) == dict, type(parsed)
    return parsed['origin']

@app.task(name='sleep_task', bind=True, ignore_result=True)
def sleep_task(self):
    time.sleep(10)

@shared_task(bind=True, max_retries=3, default_retry_delay=30)
def add_numbers(self, row_id):
    logger = get_task_logger(__name__)
    logger.info(u'[{0.id}]Function all_numbers called with params [{1}] with extended info:{0}'.format(
        self.request,
        row_id
    ))
    from .models import Adder
    record = Adder.objects.get(pk=row_id)
    record.result = record.x + record.y
    record.save()

@app.task
def add(x, y):
    return x + y


@app.task
def say(what):
    print(what)

@periodic_task(run_every=timedelta(seconds=5))
def check_status():
	url = 'http://mushfiq.com'
	res = requests.get(url)
	print res.status_code

@app.task(bind=True, default_retry_delay=300, max_retries=5)
def my_task_A(self):
    try:
        print("doing stuff here...")
    except SomeNetworkException as e:
        print("maybe do some clenup here....")
        raise self.retry(e)

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls say('hello') every 10 seconds.
    sender.add_periodic_task(10.0, say.s('hello'), name='add every 10')

    # See periodic tasks user guide for more examples:
    # http://docs.celeryproject.org/en/latest/userguide/periodic-tasks.html


from celery.schedules import crontab
from celery.task import periodic_task

@periodic_task(run_every=crontab(hour=7, minute=30, day_of_week="mon"))
def every_monday_morning():
    print("This is run every Monday morning at 7:30")

from celery.schedules import schedule


class my_schedule(schedule):

    def is_due(self, last_run_at):
        return …


if __name__ == '__main__':
    app.start()


# python myapp.py worker -l info
# python myapp.py beat -l info
# C_REMDEBUG=1 python myapp.py beat -l debug
