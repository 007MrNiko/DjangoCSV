from celery import shared_task
from DjangoCSV.celery import app
from extensions import generate_file


@shared_task
def generate_file_async(dataset_form, user_dir):
    """Celery function wrapper for simple function"""
    generate_file(dataset_form, user_dir)

