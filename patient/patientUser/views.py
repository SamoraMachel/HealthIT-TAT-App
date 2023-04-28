from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from .models import PatientUser
from datetime import datetime

import africastalking

# Create your views here.
def my_view(request):
    patients = PatientUser.objects.all()
    context = {
        "users": patients,
    }
    return render(request, "patient.html", context)

def send_message(request): 
    if request.method == 'POST':
        data = request.POST
        user_id = data.get('id')
        patient = PatientUser.objects.get(id=user_id)
        patient.dispatch_time = datetime.now()
        
        sms = africastalking.SMS
        response = sms.send(
            f"Hello {patient.username} your result are ready.\nPlease dial *384*5995# to book a date to come for \nthe results",
            [patient.phone_number]
        )
        
        
        from .producer import dispatchMessage
        dispatchMessage(
            patient, 
            response['SMSMessageData']['Recipients'][0]['messageId']
        )
        patient.save()
    return redirect("home")

def delivery_reports(request):
    data = request.get_json(force=True)
    print(f"Delivery report response...\n {data}")
    return HttpResponse(status=200)