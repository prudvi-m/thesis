from celery import shared_task
from .util import apply_script_and_update_db

@shared_task
def automate_zipfile(zipfile_id):
    # Apply automation script and update the database for the given zipfile_id
    apply_script_and_update_db(zipfile_id)
