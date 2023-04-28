"""patient URL Configuration

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
from django.urls import path

from patientUser import views as ptViews

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

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', ptViews.my_view, name="home"),
    path('dispatch/', ptViews.send_message, name="dispatch")
]
