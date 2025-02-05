from django.db import models

class Registration(models.Model):
    name=models.CharField(max_length=100)
    id_number=models.CharField(ma_length=20)
    course=models.CharField(max_length=50)
    gender=models.CharField(max_length=10)
    email=models.EmailField()

    def __str__(self):
        return self.name


# Create your models here.
