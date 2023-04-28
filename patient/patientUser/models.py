from django.db import models

# Create your models here.
class PatientUser(models.Model):
    username = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20)
    age = models.IntegerField()
    gender = models.BooleanField(choices=(
        (True, "Male"),
        (False, "Female")
    ))
    dispatch_time = models.DateTimeField(null=True, blank=True)
    
    def __str__(self) -> str:
        user_gender = "Male"
        return self.username
    
    def toString(self) -> str:
        if self.gender:
            user_gender = "Male"
        else:
            user_gender = "Female"
        return f"{self.id};{self.username};{self.phone_number};{self.age};{user_gender};{self.dispatch_time}"