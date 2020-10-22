from django.db import models

class Dane(models.Model):
    data_wyjazdu = models.CharField(max_length=30)
    data_powrotu = models.CharField(max_length=30)
    miasto = models.CharField(max_length=30)
    stopien = models.CharField(max_length=30)
    imie = models.CharField(max_length=30)
    nazwisko = models.CharField(max_length=30)
# jak cos tu zmienisz to rob manage.py makemigrations i manage.py migrate