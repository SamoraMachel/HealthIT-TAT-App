# import string

from patient.models import Patient
# from django.utils.crypto import get_random_string

from celery.utils.log import get_task_logger

from celery import shared_task
import africastalking
import time


logger = get_task_logger(__name__)


@shared_task(name="reminder task", bind=True, track_started=True)
def send_reminder_message(self, id):
    self.update_state(state='PROGRESS')
    patient = Patient.objects.get(id=id)
    time.sleep(4)
    send_reminder(patient)

    return f"Hello {patient.username} please remember to pick your test results on {patient.pick_up_date}"


def send_reminder(patient: Patient):
    sms = africastalking.SMS
    sms.send(
        f"Hello {patient.username} this is a reminder to pick your results tommorrow",
        [patient.phone_number]
    )