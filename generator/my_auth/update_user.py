import os

# funkcje odpowiedzialne za aktualizację danych użytkownika

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

from generator.forms import UpdateProfileForm, UpdateUserForm
from generator.models import UserProfile


@login_required(login_url='/login/')
def my_update(request):
    updatedUserprofile = request.user.userprofile

    if request.method == "POST":
        profileUpdateForm = UpdateProfileForm(request.POST, instance=updatedUserprofile)
        userUpdateForm = UpdateUserForm(request.POST, instance = request.user)


        if profileUpdateForm.is_valid() and userUpdateForm.is_valid():
            profileUpdateForm.save()
            userUpdateForm.save()
            messages.info(request, 'Dane zostały zapisane!')
            response = redirect('./')

            return response

    else:
        profileUpdateForm = UpdateProfileForm(instance=updatedUserprofile)
        userUpdateForm = UpdateUserForm(instance = request.user)


    return render(request, 'update.html', {"profileUpdateForm":profileUpdateForm, "userForm":userUpdateForm})
