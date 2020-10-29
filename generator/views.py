import os
from datetime import timedelta, date
from django.shortcuts import render
from django.http import HttpResponse
from django.utils.dateparse import parse_date
from docx import Document
from docx.shared import Inches, Cm, Pt


from generator.models import Dane
from .forms import BiletForm
from docxtpl import DocxTemplate
from generator.kwotaslownie import kwotaslownie

# ze zmiennej request zbiera się informacje, np kto jest zalogowany
from .maketable import dodaj_tabele
from .maketable import switch_stopien


def home_view(request, *args, **kwargs):

    return render(request, "home.html")


def generuj(request):
    form = BiletForm()
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    sample_pj = os.path.join(THIS_FOLDER, 'sample_pj.docx')
    sample_ur = os.path.join(THIS_FOLDER, 'sample_ur.docx')
    generated_doc = os.path.join(THIS_FOLDER, 'generated_doc.docx')

    if request.method == "POST":
        form = BiletForm(request.POST)
        if form.is_valid():
            typ_pociagu = form.cleaned_data.get('typ_pociagu')
            typ_autobusu = form.cleaned_data.get('typ_autobusu')
            temp_typ_srodka = ""
            srodek=""

            kwota = float(request.POST.get('kwota'))
            if typ_pociagu:
                srodek = "kolejowym w klasie 2, w pociągu "
                for i in typ_pociagu:
                    temp_typ_srodka += i + ", "
            elif typ_autobusu:
                srodek = "autobusowym w komunikacji "
                for i in typ_autobusu:
                    temp_typ_srodka += i + ", "


            typ_srodka = temp_typ_srodka[:-2]
            if request.POST.get('typ') == 'przepustkę jednorazową':
                doc = DocxTemplate(open(sample_pj,"rb"))
            elif request.POST.get('typ') == 'urlop':
                doc = DocxTemplate(open(sample_ur,"rb"))
            data_wyjazdu = request.POST.get('data_wyjazdu')
            data_powrotu = request.POST.get('data_powrotu')
            miasto = request.POST.get('miasto')
            stopien = request.POST.get('stopien')
            imie = request.POST.get('imie')
            nazwisko = request.POST.get('nazwisko')
            typ = request.POST.get('typ')
            miesiac = request.POST.get('miesiac')

            #przypisanie id stopnia do stopnia
            wyliczony_stopien = switch_stopien(stopien)
            print(wyliczony_stopien)
            #liczenie nr rozkazu batalionowego
            wstepna_data = parse_date(request.POST.get('data_wyjazdu'))
            #wstepna_data = parse_date(date(data_wyjazdu.year))
            data_rozkazu = '.............'
            nr_rozkazu = '.............'
            if wstepna_data.weekday() == 5 or wstepna_data.weekday() == 4:
                if wstepna_data.weekday() == 5:
                    data_rozkazu = wstepna_data-timedelta(days=2)
                else:
                    data_rozkazu = wstepna_data - timedelta(days=1)

                # dnia 24.09.2020 był nr rozkazu 76
                # odejmij datę wyjazdu od 24.09, uzyskane dni pocziel na 7 i pomnóż razy 2 - spodziewana liczba wydanych rozkazow
                nr_rozkazu = int(76 + (((data_rozkazu-date(2020, 9, 24)).days+1)/7)*2)

            context = {'stopien': request.POST.get('stopien'),
                           'imie':request.POST.get('imie'),
                           'nazwisko':request.POST.get('nazwisko'),
                           'adres':request.POST.get('adres'),
                           'pluton':request.POST.get('pluton'),
                            'data_przed': parse_date(request.POST.get('data_wyjazdu'))-timedelta(days=1),
                           'data_wyjazdu':request.POST.get('data_wyjazdu'),
                            'data_powrotu':request.POST.get('data_powrotu'),
                            'miesiac':request.POST.get('miesiac'),
                            'miejscowosc':request.POST.get('miasto'),
                            'kwota':kwota,
                            'kwota_slownie':kwotaslownie(kwota, 1),
                            'typ': request.POST.get('typ'),
                           'typ_srodka': typ_srodka,
                           'srodek': srodek,
                            'powrot':request.POST.get('tam_z_powrotem'),
                            'data_rozkazu':data_rozkazu,
                            'nr_rozkazu':nr_rozkazu,

                           }
            nazwisko=nazwisko.upper()
            #tworzenie obiektu bazy danych
            if typ == 'przepustkę jednorazową':
                q = Dane.objects.filter(imie=imie, nazwisko=nazwisko, typ=typ, miesiac=miesiac)
                if q.exists():  # jeśli obiekt istnieje, zaktualizuj jego dane
                    dana = Dane.objects.get(imie=imie, nazwisko=nazwisko, typ=typ, miesiac=miesiac)
                    dana.data_wyjazdu = data_wyjazdu
                    dana.data_powrotu = data_powrotu
                    dana.miasto = miasto
                    dana.stopien = stopien
                    dana.typ = typ
                    dana.transport = srodek
                    dana.miesiac=miesiac
                    dana.stopien_id = wyliczony_stopien
                    dana.save()
                else:
                    rekord = Dane(data_wyjazdu = data_wyjazdu, data_powrotu=data_powrotu, miasto=miasto, stopien=stopien, imie=imie, nazwisko=nazwisko, typ=typ, transport=srodek, miesiac=miesiac, stopien_id = wyliczony_stopien)
                    rekord.save()
            else:
                q = Dane.objects.filter(imie=imie, nazwisko=nazwisko, typ=typ, data_wyjazdu=data_wyjazdu, data_powrotu=data_powrotu)
                if q.exists():  # jeśli obiekt istnieje, zaktualizuj jego dane
                    dana = Dane.objects.get(imie=imie, nazwisko=nazwisko, typ=typ, data_wyjazdu=data_wyjazdu, data_powrotu=data_powrotu)
                    dana.data_wyjazdu = data_wyjazdu
                    dana.data_powrotu = data_powrotu
                    dana.miasto = miasto
                    dana.stopien = stopien
                    dana.typ = typ
                    dana.transport = srodek
                    dana.stopien_id = wyliczony_stopien
                    dana.save()
                else:
                    rekord = Dane(data_wyjazdu=data_wyjazdu, data_powrotu=data_powrotu, miasto=miasto, stopien=stopien,
                                  imie=imie, nazwisko=nazwisko, typ=typ, transport=srodek, stopien_id = wyliczony_stopien)
                    rekord.save()
            doc.render(context)
            doc.save(generated_doc)

            # download
            response = HttpResponse(open(generated_doc, 'rb').read())
            response['Content-Type'] = 'text/plain'
            response['Content-Disposition'] = 'attachment; filename=pobrane.docx'
            return response


    context = {
        "form": form
    }
    return render(request, "generate.html", context)

def info(request, *args, **kwargs):

    return render(request, "info.html")

def panel(request, *args, **kwargs):
    queryset1 = Dane.objects.filter(typ = 'przepustkę jednorazową').order_by('-stopien_id', 'nazwisko')
    ordered_queryset1 = queryset1
    queryset2 = Dane.objects.filter(typ = 'urlop').order_by('-stopien_id', 'nazwisko')

    context = {
        "lista": queryset1,
        "lista2":queryset2
    }
    if request.user.is_authenticated:
        return render(request, "panel.html", context)
    else:
        return render(request, "no_permission.html")

def rozkaz(request):


    query1 = Dane.objects.filter(typ = 'przepustkę jednorazową', transport = 'kolejowym w klasie 2, w pociągu ').order_by('-stopien_id', 'nazwisko')
    query2 = Dane.objects.filter(typ = 'urlop', transport = 'kolejowym w klasie 2, w pociągu ').order_by('-stopien_id', 'nazwisko')
    query3 = Dane.objects.filter(typ = 'przepustkę jednorazową', transport = 'autobusowym w komunikacji ').order_by('-stopien_id', 'nazwisko')
    query4 = Dane.objects.filter(typ = 'urlop', transport = 'autobusowym w komunikacji ').order_by('-stopien_id', 'nazwisko')


    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    generated_rozkaz = os.path.join(THIS_FOLDER, 'demo.docx')
    document = Document()

    #tworzenie tabeli osobna funkcja
    document.add_paragraph('Na PJ, pociągiem')
    table1 = dodaj_tabele(document, query1)

    document.add_paragraph('Na urlop, pociągiem')
    table2 = dodaj_tabele(document, query2)

    document.add_paragraph('Na PJ, autobusem')
    table3 = dodaj_tabele(document, query3)

    document.add_paragraph('Na urlop, autobusem')
    table4 = dodaj_tabele(document, query4)

    tables = [table1, table2, table3, table4]
    #ustawianie parametrów dokumentu
    style = document.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(12)

    i=1
    for tbl in tables:
        for row in tbl.rows:
            j=1
            for cell in row.cells:
                if j == 1: # 1)
                    cell.width = Inches(0.1)
                if j == 2: # stopien
                    cell.width = Inches(1.2)
                if j == 3: # imie
                    cell.width = Inches(1)
                if j == 4: # nazwisko
                    cell.width = Inches(1.2)
                if j == 5:
                    cell.width = Inches(2.5)
                if j == 6:
                    cell.width = Inches(0.8)
                if j == 7:
                    cell.width = Inches(1.2)
                j+=1
            i+=1

    margin = 1
    sections = document.sections
    for section in sections:
        section.top_margin = Cm(margin)
        section.bottom_margin = Cm(margin)
        section.left_margin = Cm(margin)
        section.right_margin = Cm(margin)




    #download
    document.save(generated_rozkaz)
    response = HttpResponse(open(generated_rozkaz, 'rb').read())
    response['Content-Type'] = 'text/plain'
    response['Content-Disposition'] = 'attachment; filename=rozkaz.docx'
    if request.user.is_authenticated:
        return response
    else:
        return render(request, "no_permission.html")