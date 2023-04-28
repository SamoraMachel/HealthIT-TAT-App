"""ussd URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from patient.views import delivery_report, ussd, view_patients

from patient.consumer import startConsumer
from threading import Thread

import africastalking
from django.conf import settings
aft_config : dict = settings.AFRICASTALKING


# Africa's talking configurations
def configure_aft():
    africastalking.initialize(
        aft_config['USERNAME'],
        aft_config['API_KEY']
    )
    
configure_aft()

admin.site.index_title = "TAT Administration"
admin.site.site_header = "TAT Microservice Module"
admin.site.site_title = "TAT Microservice Module"


urlpatterns = [
    path('admin/', include('smuggler.urls')),
    path('admin/', admin.site.urls),
    path("ussd/", ussd, name="ussd"),
    path('report/', delivery_report, name="report"),
    path("", view_patients, name="Home")
]

Thread(target=startConsumer, daemon=True).start()
