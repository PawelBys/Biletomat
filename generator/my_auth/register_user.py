import os

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

from generator.forms import RegisterForm


def my_register(request):

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            response = redirect('../login/')
            return response
    else:
        form = RegisterForm()
    return render(request, 'register.html', {"form":form, 'fontColor': os.getenv('FONT_COLOR')})