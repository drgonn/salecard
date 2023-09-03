import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    BROKER_URL = 'redis://redis_ocs:6379/0'
    CELERY_RESULT_BACKEND = 'redis://redis_ocs:6379/0'

    CELERY_IMPORTS = ['app.task']
    CELERYD_MAX_TASKS_PER_CHILD = 10
    CELERYBEAT_SCHEDULE = {
        'scheduled-task': {                          # 任务名, 不能重复,自由定义，在beat日志中可查看
            'task': 'app.task.task.scheduled_task',
            # 'schedule': timedelta(minutes=30)  # 每 30 分钟执行一次
            'schedule': timedelta(seconds=5)  # 每 5 秒钟执行一次
        }
    }

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True

    # Database configuration
    SQLALCHEMY_DATABASE_URI = 'postgresql://root:root@postgres_ocs:5432/ocs'

    CELERY_BROKER_URL = 'redis://redis_ocs:6379/0'


class TestingConfig(Config):
    TESTING = True

class ProductionConfig(Config):
    DEBUG = False


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

