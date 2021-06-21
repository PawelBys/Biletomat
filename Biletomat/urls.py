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

from generator.views import home_view, panel, generuj, info, rozkaz, record_delete, save_changes, wnioski, \
    baza_wnioskow, download_wniosek
from generator.my_auth.login_user import my_login
from generator.my_auth.register_user import my_register
from generator.my_auth.logout_user import my_logout
from generator.font_color_changer import change_font_color
from generator.other_documents.hdk import generuj_wniosek_hdk
from generator.other_documents.pj import generuj_wniosek_pj
from generator.other_documents.nagrodowy import generuj_wniosek_nagrodowy

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
    path('baza_wnioskow/', baza_wnioskow, name='baza_wnioskow'),
    path(r'^download_wniosek/(?P<id>[0-9]+)/$', download_wniosek, name='download_wniosek'),
    path('wnioski/hdk/', generuj_wniosek_hdk, name='hdk'),
    path('wnioski/pj/', generuj_wniosek_pj, name='pj'),
    path('wnioski/nagrodowy/', generuj_wniosek_nagrodowy, name='nagrodowy'),
    path('change_font_color/', change_font_color, name='change_font_color'),
    url(r'^delete/(?P<id>[0-9]+)/$', record_delete , name='record_delete'),
    url(r'^save/(?P<id>[0-9]+)/$', save_changes, name='save_changes'),

]
