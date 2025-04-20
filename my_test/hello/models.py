from django.db import models
from django.contrib.auth.hashers import make_password

from django.utils import timezone

# Create your models here.
class Appointments(models.Model):
    appointment_id = models.AutoField(primary_key=True, blank=True, null=False)
    national = models.ForeignKey('Donors', models.DO_NOTHING, to_field='national_id')
    appointment_date = models.DateTimeField(max_length=100)
    center_name = models.CharField(max_length=100)
    status = models.TextField()

    
    

    class Meta:
        managed = False
        db_table = 'Appointments'


class Donations(models.Model):
    donation_id = models.AutoField(primary_key=True, blank=True, null=False)
    national = models.ForeignKey('Donors', models.DO_NOTHING, to_field='national_id')
    donation_date = models.TextField(blank=True, null=True, max_length=100)  # This field type is a guess.
    blood_type = models.TextField(blank=True, null=True, max_length=100)
    quantity = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'Donations'


class Feedback(models.Model):
    feedback_id = models.AutoField(primary_key=True, blank=True, null=False)
    national = models.ForeignKey('Donors', models.DO_NOTHING, to_field='national_id')
    feedback_text = models.TextField()
    submission_date = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'Feedback'

class Donors(models.Model):
    id=models.AutoField( primary_key=True)
    national_id = models.CharField(unique=True, max_length=100)
    username = models.CharField(unique=True, max_length=100)
    email=models.EmailField(unique=True,max_length=100)
    password = models.CharField(max_length=100)
    date_joined=models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.username
    class Meta:
        managed = True
        db_table = 'donors'


class USER(models.Model):
    name=models.CharField(max_length=100)
    age=models.IntegerField()
    id_number=models.CharField(max_length=100,unique=True)
    gender=models.CharField(max_length=100)
    location=models.CharField(max_length=100)
    phone=models.CharField(max_length=15 ,default="0000000000")
    center=models.CharField(max_length=100) 
    
    def __str__ (self):
        return self.name
    
    class Meta:
        managed = True
        db_table = 'USER'

class REQUESTS(models.Model):
    name=models.CharField(max_length=100)
    idNumber=models.CharField(max_length=15)
    email=models.CharField(max_length=15)
    phone=models.CharField(max_length=15)
    gender=models.CharField(max_length=100)
    bloodType=models.CharField(max_length=20)
    location=models.CharField(max_length=100)
    address=models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    class Meta:
        managed=True
        db_table='REQUESTS'

    


def Auth(email, password) -> bool:
    if Donors.objects.filter(email=email).exists():
        client = Donors.objects.get(email=email)
        if client.password == password:

            client:dict = list(Donors.objects.filter(email=email))[0]
            print(client)
            return True
    
    return False
