from __future__ import absolute_import

from celery import Celery

print 'in proj.celery'

app = Celery('exploratory_analysis',
             broker='amqp://',
             backend='amqp://',
             include=['exploratory_analysis.tasks'])

# Optional configuration, see the application user guide.
app.conf.update(
    CELERY_TASK_RESULT_EXPIRES=3600,
)

if __name__ == '__main__':
    app.start()