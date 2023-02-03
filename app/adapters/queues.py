from celery import Celery
from celery import current_app as curernt_celery_app

from app import config


def create_celery():
    celery: Celery = curernt_celery_app
    celery.config_from_object(config, namespace="CELERY")
    return celery
