from app import create_app
from app.extensions import celery

app = create_app('default')
celery = make_celery(app)    