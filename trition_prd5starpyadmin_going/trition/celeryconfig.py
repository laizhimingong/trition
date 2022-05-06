from datetime import timedelta

import djcelery

djcelery.setup_loader()

# 导入任务
CELERY_IMPORTS = [
    'alert.tasks',
]
# 设置队列
CELERY_QUEUES = {
    'beat_tasks': {
        'exchange': 'beat_tasks',
        'exchange_type': 'direct',
        'binding_key': 'beat_tasks'
    },
    'work_queue': {
        'exchange': 'work_queue',
        'exchange_type': 'direct',
        'binding_key': 'work_queue'
    }
}
# 设置默认列队,不符合其他队列的任务放在默认队列
CELERY_DEFAULT_QUEUE = 'work_queue'

# 有些情况下可以防止死锁
CELERYD_FORCE_EXECV = True

# 设置并发数量
CELERYD_CONCURRENCY = 10

# 每个worker最多执行100个任务，防止泄露内存
CELERYD_MAX_TASKS_PER_CHILD = 100

# 单个任务最多执行时间
CELERYD_TASK_TIME_LIMIT = 12 * 30

# 设置定时执行
CELERYBAET_SCHEDULE = {
    'task1': {
        'task': 'course-task',
        'schedule': timedelta(seconds=5),
        'options': {
            'queue': 'beat_tasks'
        }
    }
}
CELERY_TIMEZONE = 'Asia/Shanghai'
CELERY_TASK_SERIALIZER = 'pickle'
CELERY_RESULT_SERIALIZER = 'pickle'
CELERY_ACCEPT_CONTENT = ['pickle', 'json', ]

BROKER_BACKEND = 'redis'
BROKER_URL = 'redis://127.0.0.1:6379/3'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/2'
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
