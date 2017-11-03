# Celery settings
from kombu import Exchange
from kombu import Queue



BROKER_URL = 'redis://127.0.0.1:6379/6'
# 可见性超时时间定义了等待职程在消息分派到其他职程之前确认收到任务的秒数。一定要阅读下面的 警示 一节。
# 这个选项通过 BROKER_TRANSPORT_OPTIONS 设置:

BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}  # 1 hour.

CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/5'

CELERY_QUEUE_HA_POLICY = 'all'
CELERY_ACKS_LATE = True
CELERY_RESULT_PERSISTENT = True
CELERYD_PREFETCH_MULTIPLIER = 1

CELERYD_CONCURRENCY = 4



CELERY_TIMEZONE = 'Asia/Shanghai'
CELERY_ENABLE_UTC = True

# 读取任务结果一般性能要求不高，所以使用了可读性更好的JSON
CELERY_RESULT_SERIALIZER = 'json'

# 指定接受的内容类型
CELERY_ACCEPT_CONTENT = ['json', 'msgpack', 'yaml', 'pickle']

# 任务序列化和反序列化使用msgpack方案
CELERY_TASK_SERIALIZER = 'msgpack'

# 任务过期时间，不建议直接写86400，应该让这样的magic数字表述更明显
CELERY_TASK_RESULT_EXPIRES = 60 * 60 * 24

CELERY_IMPORTS = ("tasks",)
CELERY_ANNOTATIONS = {'tasks.add': {'rate_limit': '10/s'}}
CELERY_ANNOTATIONS = {'*': {'rate_limit': '10/s'}}
def my_on_failure(self, exc, task_id, args, kwargs, einfo):
    print('Oh no! Task failed: {0!r}'.format(exc))

CELERY_ANNOTATIONS = {'*': {'on_failure': my_on_failure}}

class MyAnnotate(object):

    def annotate(self, task):
        if task.name.startswith('tasks.'):
            return {'rate_limit': '10/s'}

CELERY_ANNOTATIONS = (MyAnnotate(), {…})


CELERY_DEFAULT_QUEUE = 'default'
CELERY_QUEUES = (
    Queue('default', Exchange('default'), routing_key='default'),
    Queue('for_task_A', Exchange('for_task_A'), routing_key='for_task_A'),
    Queue('for_task_B', Exchange('for_task_B'), routing_key='for_task_B'),

    # 路由键以“task.”开头的消息都进default队列
    Queue('default', routing_key='task.#'),

    # 路由键以“web.”开头的消息都进web_tasks队列
    Queue('web_tasks', routing_key='web.#'),
)
CELERY_DEFAULT_EXCHANGE = 'tasks'  # 默认的交换机名字为tasks
CELERY_DEFAULT_EXCHANGE_TYPE = 'topic'  # 默认的交换类型是topic
CELERY_DEFAULT_ROUTING_KEY = 'task.default'  # 默认的路由键是task.default，这个路由键符合上面的default队列

CELERY_ROUTES = {
    'my_taskA': {'queue': 'for_task_A', 'routing_key': 'for_task_A'},
    'my_taskB': {'queue': 'for_task_B', 'routing_key': 'for_task_B'},
    'projq.tasks.add': {  # tasks.add的消息会进入web_tasks队列
        'queue': 'web_tasks',
        'routing_key': 'web.add',
    }
}

from datetime import timedelta
from celery.schedules import crontab

CELERYBEAT_SCHEDULE = {
    'add-every-30-seconds': {
        'task': 'proj.tasks.add',
        'schedule': timedelta(seconds=30),
        'args': (16, 16)
    },
    # Executes every Monday morning at 7:30 A.M
    'add-every-monday-morning': {
        'task': 'tasks.add',
        'schedule': crontab(hour=7, minute=30, day_of_week=1),
        'args': (16, 16),
    },

    # CELERYBEAT_SCHEDULE中指定了tasks.add这个任务每10秒跑一次，执行的时候的参数是16和16
    # 启动Beat程序：celery beat -A projb
    'add': {
        'task': 'projb.tasks.add',
        'schedule': timedelta(seconds=10),
        'args': (16, 16)
    }
}




# 最后再为每个task启动不同的workerscelery worker -E -l INFO -n workerA -Q for_task_A celery worker -E -l INFO -n workerB -Q for_task_B
# 自动重载功能，pip install pyinotify
# env CELERYD_FSNOTIFY=stat celery worker -l info --autoreload

"""
app.control.broadcast('pool_restart',arguments={'modules': ['foo', 'bar']})
app.control.broadcast('pool_restart', arguments={'reload': True})
app.control.broadcast('pool_restart',arguments={'modules': ['foo'],'reload': True})
app.control.broadcast('rate_limit',arguments={'task_name': 'myapp.mytask','rate_limit': '200/m'})
app.control.broadcast('rate_limit', {'task_name': 'myapp.mytask', 'rate_limit': '200/m'}, reply=True)
>>> app.control.time_limit('tasks.crawl_the_web',
                           soft=60, hard=120, reply=True)
[{'worker1.example.com': {'ok': 'time limits set successfully'}}]
app.control.rate_limit('myapp.mytask', '200/m')



# 工作流
from celery import signature
signature('tasks.add', args=(2, 2), countdown=10)
add.subtask((2, 2), countdown=10)
add.s(2, 2)
add.s(2, 2, debug=True)
s = add.subtask((2, 2), {'debug': True}, countdown=10)
>>> s.args
(2, 2)
>>> s.kwargs
{'debug': True}
>>> s.options
{'countdown': 10}

from celery import chain
res = chain(add.s(2, 2), add.s(4), add.s(8))()
res.get()

(add.s(2, 2) | add.s(4) | add.s(8))().get()

add.subtask((2, 2), immutable=True)


>>> res = (add.si(2, 2) | add.si(4, 4) | add.s(8, 8))()
>>> res.get()
16

>>> res.parent.get()
8

>>> res.parent.parent.get()
4


>>> from celery import group
>>> res = group(add.s(i, i) for i in xrange(10))()
>>> res.get(timeout=1)
[0, 2, 4, 6, 8, 10, 12, 14, 16, 18]


celery worker --loglevel=INFO --concurrency=10 -n worker1.%h
ps auxww | grep 'celery worker' | awk '{print $2}' | xargs kill -9
kill -HUP $pid



>>> result.revoke()

>>> AsyncResult(id).revoke()

>>> app.control.revoke('d9078da5-9915-40a0-bfa1-392c7bde42ed')

>>> app.control.revoke('d9078da5-9915-40a0-bfa1-392c7bde42ed',
...                    terminate=True)

>>> app.control.revoke('d9078da5-9915-40a0-bfa1-392c7bde42ed',
...                    terminate=True, signal='SIGKILL')

app.control.revoke([
...    '7993b0aa-1f0b-4780-9af0-c47c0858b3f2',
...    'f565793e-b041-4b2b-9ca4-dca22762a55d',
...    'd9d35e03-2997-42d0-a13e-64a66b88a618',
])




--autoscale=AUTOSCALE
     Enable autoscaling by providing
     max_concurrency,min_concurrency.  Example:
       --autoscale=10,3 (always keep 3 processes, but grow to
      10 if necessary).


      >>> myapp.control.add_consumer(
...     queue='baz',
...     exchange='ex',
...     exchange_type='topic',
...     routing_key='media.*',
...     options={
...         'queue_durable': False,
...         'exchange_durable': False,
...     },
...     reply=True,
...     destination=['w1@example.com', 'w2@example.com'])


celery worker -P eventlet -c 1000


celery multi start worker1 \
    --pidfile="$HOME/run/celery/%n.pid" \
    --logfile=""$HOME/log/celery/%n.log"


# Create graph of currently installed bootsteps in both the worker
# and consumer namespaces.
$ celery graph bootsteps | dot -T png -o steps.png

# Graph of the consumer namespace only.
$ celery graph bootsteps consumer | dot -T png -o consumer_only.png

# Graph of the worker namespace only.
$ celery graph bootsteps worker | dot -T png -o worker_only.png



# Create graph from the current cluster
$ celery graph workers | dot -T png -o workers.png

# Create graph from a specified list of workers
$ celery graph workers nodes:w1,w2,w3 | dot -T png workers.png

# also specify the number of threads in each worker
$ celery graph workers nodes:w1,w2,w3 threads:2,4,6

# …also specify the broker and backend URLs shown in the graph
$ celery graph workers broker:amqp:// backend:redis://

# …also specify the max number of workers/threads shown (wmax/tmax),
# enumerating anything that exceeds that number.
$ celery graph workers wmax:10 tmax:3

"""