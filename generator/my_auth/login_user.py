import os

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from Biletomat import settings
from generator.forms import LoginForm


def my_login(request):
    response = redirect('/')
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = LoginForm(request.POST)

            if form.is_valid():

                username = request.POST.get('login')
                password = request.POST.get('password')
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return response
                else:
                    messages.info(request, 'Nieprawidłowe hasło!')
                    return render(request, "login.html", {'form': LoginForm(request.POST), 'fontColor': os.getenv('FONT_COLOR')})
                return
            else:
                return render(request, "no_permission.html", {'fontColor': os.getenv('FONT_COLOR')})
        return render(request, "login.html", {'form': LoginForm(), 'fontColor': os.getenv('FONT_COLOR')})
    else:
        return response