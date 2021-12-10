"""Biletomat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path

from generator.my_auth.password_reset import password_reset_request
from generator.views import home_view, panel, generuj, info, rozkaz, record_delete, save_changes, wnioski, \
    baza_wnioskow, download_wniosek, record_edit
from generator.my_auth.login_user import my_login
from generator.my_auth.register_user import my_register
from generator.my_auth.logout_user import my_logout
from generator.my_auth.update_user import my_update
from generator.other_documents.hdk import generuj_wniosek_hdk
from generator.other_documents.pj import generuj_wniosek_pj
from generator.other_documents.nagrodowy import generuj_wniosek_nagrodowy
from django.contrib.auth import views as auth_views

# tutaj dodaje się kolejne "widoki" - podstrony, trzeba je mieć w pliku views jako funkcję

app_name = 'generator'

urlpatterns = [
    path('home/', home_view, name='home_view'),
    path('', home_view, name='home_view'),
    path('panel/', panel, name='panel'),
    path('admin/', admin.site.urls),
    path('generuj/', generuj, name='generuj'),
    path('info/', info, name='info'),
    path('rozkaz/', rozkaz, name='rozkaz'),
    path('no_permission/', panel, name='panel'),
    path('wnioski/', wnioski, name='wnioski'),
    path('login/', my_login, name='login'),
    path('register/', my_register, name='register'),
    path('logout/', my_logout, name='logout'),
    path('update/', my_update, name='update'),
    path('baza_wnioskow/', baza_wnioskow, name='baza_wnioskow'),
    path(r'^download_wniosek/(?P<id>[0-9]+)/$', download_wniosek, name='download_wniosek'),
    path('wnioski/hdk/', generuj_wniosek_hdk, name='hdk'),
    path('wnioski/pj/', generuj_wniosek_pj, name='pj'),
    path('wnioski/nagrodowy/', generuj_wniosek_nagrodowy, name='nagrodowy'),
    url(r'^delete/(?P<id>[0-9]+)/$', record_delete , name='record_delete'),
    url(r'^save/(?P<id>[0-9]+)/$', save_changes, name='save_changes'),
    url(r'^edit/(?P<id>[0-9]+)/$', record_edit, name='record_edit'),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="password/password_reset_confirm.html"),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='password/password_reset_complete.html'),
         name='password_reset_complete'),
    path("password_reset/", password_reset_request, name="password/password_reset"),

]
