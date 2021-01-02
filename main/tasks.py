from celery import shared_task
from DjangoCSV.celery import app
from extensions import generate_file

#@app.task(ignore_result=True)
@shared_task
def generate_file_async(dataset_form, user_dir):
    generate_file(dataset_form, user_dir)

