from django.db import models

# Create your models here.
class Enquiry(models.Model):
    submission_date=models.DateField(auto_now_add=True)
    submission_time=models.TimeField(auto_now_add=True)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phoneNumber = models.CharField(max_length=15, null=False, blank=False)
    location = models.CharField(max_length=200,null=False,blank=False)    
    registration = models.CharField(max_length=225, null=False,blank=False)
    requirement = models.CharField(max_length=255,null=False, blank=False)

    read = models.BooleanField(default = False)


    def __str__(self):
        return self.name

