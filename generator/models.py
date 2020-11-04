from django.db import models

class Dane(models.Model):
    data_wyjazdu = models.CharField(max_length=30)
    data_powrotu = models.CharField(max_length=30)
    miasto = models.CharField(max_length=30)
    stopien = models.CharField(max_length=30)
    imie = models.CharField(max_length=30)
    nazwisko = models.CharField(max_length=30)
    typ = models.CharField(max_length=30)
    transport = models.CharField(max_length=30)
    miesiac = models.CharField(max_length=30, default='---')
    stopien_id = models.CharField(max_length=10)
    nr_rozkazu = models.CharField(max_length=10)
    doniesione = models.CharField(max_length=1, default="")
# jak cos tu zmienisz to rob manage.py makemigrations i manage.py migrate