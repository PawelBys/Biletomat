from django.db import models

class Dane(models.Model):
    data_wyjazdu = models.CharField(max_length=30)
    data_powrotu = models.CharField(max_length=30)
    miasto = models.CharField(max_length=30)
    stopien = models.CharField(max_length=30)
    imie = models.CharField(max_length=30)
    nazwisko = models.CharField(max_length=30)
    adres = models.CharField(max_length=100)
    pododdzial =models.CharField(max_length=20)
    miesiac = models.CharField(max_length=20)
    kwota = models.DecimalField(decimal_places=2, max_digits=10)
    kwota_slownie = models.CharField(max_length=40)
# jak cos tu zmienisz to rob manage.py makemigrations i manage.py migrate