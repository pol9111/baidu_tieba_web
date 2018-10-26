from celery import Celery
from config import BROKER, BACKEND

app = Celery('crawl_task', include=['scheduler'], broker=BROKER, backend=BACKEND)
# 官方推荐使用json作为消息序列化方式

app.conf.update(
    CELERY_TIMEZONE='Asia/Shanghai',
    CELERY_ENABLE_UTC=True,
    CELERY_ACCEPT_CONTENT=['json'],
    CELERY_TASK_SERIALIZER='json',
    CELERY_RESULT_SERIALIZER='json',
    CELERY_TASK_RESULT_EXPIRES = 60 * 60 * 24  # 任务过期时间，不建议直接写86400，应该让这样的magic数字表述更明显

)