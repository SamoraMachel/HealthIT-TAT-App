from django.http import HttpResponse, QueryDict
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import Patient
from datetime import datetime
import datetime as DT

from .models import Patient
from .task import send_reminder_message

from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)

import pytz

# Create your views here.
@csrf_exempt
def delivery_report(request):
    data = request.POST
    patient: Patient = Patient.objects.get(messageId=data.get("id", None), phone_number=data.get("phoneNumber", None))
    if patient:
        patient.status = data.get("status", None)
        fail_reason = data.get("failureReason", None)
        patient.failure_reason = fail_reason
        if fail_reason == None:
            patient.time_delivered = datetime.now()
        patient.network_code = data.get('networkCode', None)
        patient.save()
    return HttpResponse(status=200)

@csrf_exempt
def ussd(request):
    response = ""
    data: QueryDict = request.POST
    session_id = data.get("sessionId", None)
    service_code = data.get("serviceCode", None)
    phone_number = data.get("phoneNumber", None)
    
    patient: Patient = Patient.objects.filter(phone_number=phone_number).first()
    
    timezone = pytz.timezone("Africa/Nairobi")
    current_date = datetime.now(timezone)
    patient.interaction_time = current_date
    
    tat_calc: DT.timedelta = patient.interaction_time - patient.dispatch_time
    patient.TAT = tat_calc.total_seconds()
    
    text = data.get("text", "default")
    if text == '':
        response  = f"CON Dear {patient.username} your test results are ready. Kindly enter the day when you'll be able to collect them \n"
        response += "1. 1 day \n"
        response += "2. 4 days \n"
        response += "3. 7 days \n"
        response += "4. 14 days \n"
        response += "00. Opt Out \n"
        result = send_reminder_message.delay(patient.id)
        print(result.state)

    elif text == '1':
        response = "END Dear patient thank you for your response, we expect you in a days time"
        patient.pick_up_date = datetime.now().date() + DT.timedelta(days=1)
    elif text == '2':
        response = "END Dear patient thank you for your response, we expect you within 4 days"
        patient.pick_up_date = datetime.now().date() + DT.timedelta(days=4)
    elif text == '3':
        response = "END Dear patient thank you for your response, we expect you within 7 days"
        patient.pick_up_date = datetime.now().date() + DT.timedelta(days=7)
    elif text == '4':
        response = "END Dear patient thank you for your response, we expect you within 14 days"
        patient.pick_up_date = datetime.now().date() + DT.timedelta(days=14)
    elif text == '00':
        response = "END Your have opt Out Successfully"
    else:
        response = "CON Not a valid Response. Select one from below.\n"
        response += "1. 1 day \n"
        response += "2. 4 days \n"
        response += "3. 7 days \n"
        response += "4. 14 days \n"
        response += "00. Opt Out \n"
    patient.save()
    return HttpResponse(response)


def view_patients(request):
    pt_list = Patient.objects.all()
    return render(request, 'tat.html', {
        "patients": pt_list
    })