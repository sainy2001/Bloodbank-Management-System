from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


# Create your models here.

class custom_user(models.Model):
    email = models.EmailField(max_length=150, primary_key=True)
    user_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=10, unique=True)
    password = models.CharField(max_length=50)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user_name


class login_session(models.Model):
    user = models.ForeignKey(custom_user, on_delete=models.CASCADE)
    login_time = models.DateTimeField(default=timezone.now)
    logout_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.user_name}'s Login Session"


class Bloodbank_System(models.Model):
    district_id = models.CharField(max_length=50, primary_key=True)
    district_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.district_id


class Bloodbank_Details(models.Model):
    bloodbank_id = models.CharField(max_length=50, primary_key=True)
    bloodbank_name = models.CharField(max_length=100)
    district = models.ForeignKey(Bloodbank_System, on_delete=models.CASCADE)
    address = models.CharField(max_length=200)
    mobile = models.CharField(max_length=13)
    email = models.EmailField(max_length=50)

    def __str__(self):
        return self.bloodbank_id


class Blood_Group_Details(models.Model):
    product_id = models.CharField(max_length=50, primary_key=True)
    product_name = models.CharField(max_length=50, unique=True)
    donated_blood_to = models.CharField(max_length=100)
    received_blood_from = models.CharField(max_length=100)

    def __str__(self):
        return self.product_id


class Blood_Stuck_Details(models.Model):
    blood_group = models.ForeignKey(Blood_Group_Details, on_delete=models.CASCADE)
    bloodbank = models.ForeignKey(Bloodbank_Details, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=10)
    amount = models.CharField(max_length=10)


class Doctor_Details(models.Model):
    doctorid = models.CharField(max_length=10, primary_key=True)
    d_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1)
    specialization = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=13)
    address = models.CharField(max_length=100)

    def __str__(self):
        return self.doctorid
    
class Donor_Details(models.Model):
    donorid = models.CharField(max_length=10, primary_key=True)
    do_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1)
    blood_group = models.CharField(max_length=4)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=13)
    address = models.CharField(max_length=100)
    
    def __str__(self):
        return self.donorid