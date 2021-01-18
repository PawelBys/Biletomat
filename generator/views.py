import os
from datetime import  date
from django.shortcuts import render, redirect
from django.http import HttpResponse

from docx import Document

from docx.shared import Inches, Cm, Pt
from docx.enum.table import WD_ROW_HEIGHT
from Biletomat import settings
from generator.models import Dane
from .forms import BiletForm


# ze zmiennej request zbiera się informacje, np kto jest zalogowany
from .maketable import dodaj_tabele, dodaj_naglowek, dodaj_stopke, switch_litery
from .generate_request import generuj_ext


def home_view(request, *args, **kwargs):
    context = {
        'data' : settings.DATA_GRANICZNA.strftime("%d.%m.%Y")
    }
    return render(request, "home.html", context)


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
            response['Content-Disposition'] = 'attachment; filename=pobrane.docx'

            return response

    context = {
        "form": form
    }
    if date.today() > data and not request.user.is_authenticated:
        return render(request, "no_permission.html")
    else:
        return render(request, "generate.html", context)

def info(request, *args, **kwargs):

    return render(request, "info.html")

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
    queryset2 = Dane.objects.filter(typ = 'urlop').order_by('nr_rozkazu', 'nazwisko')

    context = {
        "lista": queryset1,
        "lista2":queryset2
    }
    if request.user.is_authenticated:
        return render(request, "panel.html", context)
    else:
        return render(request, "no_permission.html")

# generowanie pliku word z rozkazem
def rozkaz(request):

    query1 = Dane.objects.filter(typ = 'przepustkę jednorazową', transport = 'kolejowym w klasie 2, w pociągu ').order_by('-stopien_id', 'nazwisko')
    query2 = Dane.objects.filter(typ = 'urlop', transport = 'kolejowym w klasie 2, w pociągu ').order_by('-stopien_id', 'nazwisko')
    query3 = Dane.objects.filter(typ = 'przepustkę jednorazową', transport = 'autobusowym w komunikacji ').order_by('-stopien_id', 'nazwisko')
    query4 = Dane.objects.filter(typ = 'urlop', transport = 'autobusowym w komunikacji ').order_by('-stopien_id', 'nazwisko')

    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    generated_rozkaz = os.path.join(THIS_FOLDER, 'demo.docx')
    document = Document()

    dodaj_naglowek(document)

    licznik = 1

    tables =[]

    #tworzenie tabeli osobna funkcja
    if query1:
        p = document.add_paragraph( switch_litery(licznik) + 'na przepustkę jednorazową – środek transportu PKP:')
        #p.paragraph_format.left_indent = Inches (0.25)
        table1 = dodaj_tabele(document, query1)
        tables.append(table1)
        p.paragraph_format.space_before = Pt(12)

    if query2:
        licznik+=1
        p = document.add_paragraph( switch_litery(licznik) + 'na urlop – środek transportu PKP:')
        #p.paragraph_format.left_indent = Inches (0.25)
        table2 = dodaj_tabele(document, query2)
        tables.append(table2)
        p.paragraph_format.space_before = Pt(12)
    if query3:
        licznik += 1
        p = document.add_paragraph( switch_litery(licznik) + 'na przepustkę jednorazową – środek transportu PKS:')
        #p.paragraph_format.left_indent = Inches (0.25)
        table3 = dodaj_tabele(document, query3)
        tables.append(table3)
        p.paragraph_format.space_before = Pt(12)
    if query4:
        licznik += 1
        p = document.add_paragraph( switch_litery(licznik) + 'na urlop – środek transportu PKS:')
        #p.paragraph_format.left_indent = Inches (0.25)
        table4 = dodaj_tabele(document, query4)
        tables.append(table4)
        p.paragraph_format.space_before = Pt(12)

    #ustawianie parametrów dokumentu
    style = document.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(12)

    #ustawianie szerokosci tabelek
    i=1
    for tbl in tables:
        for row in tbl.rows:
            j=1
            row.height_rule = WD_ROW_HEIGHT.EXACTLY
            row.height = Inches(0.20)
            for cell in row.cells:
                if j == 1: # 1)
                    cell.width = Inches(0.1)
                if j == 2: # stopien
                    cell.width = Inches(1.25)
                if j == 3: # imie
                    cell.width = Inches(0.9)
                if j == 4: # nazwisko
                    cell.width = Inches(1.5)
                if j == 5:
                    cell.width = Inches(2.4)
                if j == 6:
                    cell.width = Inches(0.6)
                if j == 7:
                    cell.width = Inches(1.2)
                j+=1
            i+=1

    dodaj_stopke(document)
    # ustawianie marginesow
    sections = document.sections
    for section in sections:
        section.top_margin = Cm(1.5)
        section.bottom_margin = Cm(1.59)
        section.left_margin = Cm(0.75)
        section.right_margin = Cm(1.32)

    #download
    document.save(generated_rozkaz)
    response = HttpResponse(open(generated_rozkaz, 'rb').read())
    response['Content-Type'] = 'text/plain'
    response['Content-Disposition'] = 'attachment; filename=rozkaz.docx'
    if request.user.is_authenticated:
        return response
    else:
        return render(request, "no_permission.html")