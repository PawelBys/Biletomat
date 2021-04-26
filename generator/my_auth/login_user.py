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
                    return render(request, "login.html", {'form': LoginForm(request.POST)})
                return
            else:
                return render(request, "no_permission.html")
        return render(request, "login.html", {'form': LoginForm()})
    else:
        return response