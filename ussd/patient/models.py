from django.db import models

# Create your models here.
class Patient(models.Model):
    username = models.CharField(max_length=200, blank=True, null=True)
    phone_number = models.CharField(max_length=20)
    gender = models.CharField(max_length=6)
    age = models.IntegerField()
    
    dispatch_time = models.DateTimeField()
    messageId = models.CharField(max_length=200)
    time_delivered = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True)
    network_code = models.CharField(max_length=100, blank=True, null=True)
    failure_reason = models.CharField(max_length=200, blank=True, null=True)
    
    interaction_time = models.DateTimeField(blank=True, null=True)
    pick_up_date = models.DateField(blank=True, null=True)
    
    TAT = models.FloatField(blank=True, null=True)
    
    def __str__(self) -> str:
        return self.username