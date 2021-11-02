import os

from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

from generator.forms import UpdateForm
from generator.models import UserProfile


def my_update(request):
    updatedUserprofile = request.user.userprofile

    if request.method == "POST":
        form = UpdateForm(request.POST, instance=updatedUserprofile)
        if form.is_valid():
            form.save()
            messages.info(request, 'Dane zostały zapisane!')
            response = redirect('./')
            return response
    else:
        form = UpdateForm(instance=updatedUserprofile)

    return render(request, 'update.html', {"form":form})