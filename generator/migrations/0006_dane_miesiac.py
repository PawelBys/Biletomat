# Generated by Django 3.1.2 on 2020-10-28 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('generator', '0005_dane_transport'),
    ]

    operations = [
        migrations.AddField(
            model_name='dane',
            name='miesiac',
            field=models.CharField(default='styczen', max_length=30),
            preserve_default=False,
        ),
    ]
