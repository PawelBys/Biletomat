# Generated by Django 3.1.2 on 2021-05-24 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('generator', '0012_dane_osobowe_rightssupport'),
    ]

    operations = [
        migrations.CreateModel(
            name='FontColor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(max_length=30)),
            ],
        ),
    ]