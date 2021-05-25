from django.contrib.auth.models import User
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

class Dane_osobowe (models.Model):
    imie = models.CharField(max_length=30)
    nazwisko = models.CharField(max_length=30)
    stopien = models.CharField(max_length=30)
    pluton = models.CharField(max_length=1)
    wydzial = models.CharField(max_length=5)
    grupa = models.CharField(max_length=10)

class RightsSupport(models.Model):
    class Meta:
        managed = False  # No database table creation or deletion  \
        # operations will be performed for this model.

        default_permissions = ()  # disable "add", "change", "delete"
        # and "view" default permissions

        permissions = (
            ('user_rights', 'Globalne uprawnienia użytkownika'),

        )

class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    imie = models.CharField(max_length=30)
    nazwisko = models.CharField(max_length=30)
    adres = models.CharField(max_length=100, default='')
    stopien = models.CharField(max_length=30)
    pluton = models.CharField(max_length=1)
    wydzial = models.CharField(max_length=5)
    grupa = models.CharField(max_length=10)
