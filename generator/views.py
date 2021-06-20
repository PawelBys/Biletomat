import os
from datetime import  date

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse

from docx import Document

from docx.shared import Inches, Cm, Pt
from docx.enum.table import WD_ROW_HEIGHT
from Biletomat import settings
from Biletomat.settings import FONT_COLOR
from generator.models import Dane
from .forms import BiletForm
import datetime
import calendar


# ze zmiennej request zbiera się informacje, np kto jest zalogowany
from .maketable import dodaj_tabele, dodaj_naglowek, dodaj_stopke, switch_litery
from .generate_request import generuj_ext, generuj_rozkaz




def home_view(request, *args, **kwargs):
    context = {
        'data' : settings.DATA_GRANICZNA.strftime("%d.%m.%Y"),
        'fontColor': os.getenv('FONT_COLOR')
    }

    # jesli uzytkownik jest zalogowany, to wyswietl normalna strone
    return render(request, "home.html", context)
    # jesli jest niezalogowany, to wyswietl okrojona wersje


def generuj(request):
    form = BiletForm()
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

    generated_doc = os.path.join(THIS_FOLDER, 'generated_doc.docx')

    data = settings.DATA_GRANICZNA

    if request.method == "POST":
        form = BiletForm(request.POST)
        if form.is_valid():

            #wywołanie metody odpowiedzialnej za generowanie
            generuj_ext(request, form, generated_doc)

            # download
            response = HttpResponse(open(generated_doc, 'rb').read())
            response['Content-Type'] = 'text/plain'

            response['Content-Disposition'] = 'attachment; filename = wniosek.docx'

            return response


    context = {
        "form": form,
        'fontColor': os.getenv('FONT_COLOR'),
        'typ_wniosku': 'Wniosek o zwrot kosztów przejazu'
    }
    if date.today() > data and not request.user.is_authenticated:
        return render(request, "no_permission.html")
    else:
        return render(request, "generate.html", context)


def info(request, *args, **kwargs):

    context = {
        'fontColor': os.getenv('FONT_COLOR')
    }
    return render(request, "info.html", context)

#funkcja do usuwania rekordow
def record_delete(request, id):
    object = Dane.objects.filter(id=id)
    if request.method =='POST':
        object.delete()
        return redirect('/panel')

# funkcja odpowiedzialna za zaznaczanie, kto już przyniósł mi wniosek
def save_changes(request, id):
    object = Dane.objects.get(id=id)

    if request.method =='POST':
        if object.doniesione == "X":
            object.doniesione = ""
        else:
            object.doniesione = "X"
        object.save()
        return redirect('/panel')

# funkcja odpowiedzialna za widok administratora
def panel(request, *args, **kwargs):
    queryset1 = Dane.objects.filter(typ = 'przepustkę jednorazową').order_by('nr_rozkazu', 'nazwisko')
    ordered_queryset1 = queryset1
    queryset2 = Dane.objects.filter(typ = 'urlop').order_by('data_wyjazdu', 'nazwisko')

    context = {
        "lista": queryset1,
        "lista2":queryset2,
        'fontColor': os.getenv('FONT_COLOR')
    }
    if request.user.is_superuser:
        return render(request, "panel.html", context)
    else:
        return render(request, "no_permission.html")

# generowanie pliku word z rozkazem
def rozkaz(request):

# osobna metoda w pliku generate_request
    if request.user.is_superuser:
        return generuj_rozkaz(request)
    else:
        return render(request, "no_permission.html")


def wnioski(request):



    return render(request, "wniosek.html")
