import os
from datetime import timedelta
from django.shortcuts import render
from django.http import HttpResponse
from django.utils.dateparse import parse_date
from docx import Document
from docx.shared import Inches, Cm, Pt
from docx.text import font

from generator.models import Dane
from .forms import BiletForm
from docxtpl import DocxTemplate
from generator.kwotaslownie import kwotaslownie

# ze zmiennej request zbiera się informacje, np kto jest zalogowany

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

                       }
        #tworzenie obiektu bazy danych
        q = Dane.objects.filter(imie=imie, nazwisko=nazwisko)
        if q.exists():  # jeśli obiekt istnieje, zaktualizuj jego dane
            dana = Dane.objects.get(imie=imie)
            dana.data_wyjazdu = data_wyjazdu
            dana.data_powrotu = data_powrotu
            dana.miasto = miasto
            dana.stopien = stopien
            dana.save()
        else:
            rekord = Dane(data_wyjazdu = data_wyjazdu, data_powrotu=data_powrotu, miasto=miasto, stopien=stopien, imie=imie, nazwisko=nazwisko)
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
    queryset = Dane.objects.all()

    context = {
        "lista": queryset,
    }
    return render(request, "panel.html", context)

def rozkaz(request):
    queryset = Dane.objects.all()


    #queryset = Dane.objects.values_list('stopien', 'imie', 'nazwisko', 'data_wyjazdu', 'data_powrotu', 'miasto') # ogranicz to do wpisów z ostatnich 3 dni
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    generated_rozkaz = os.path.join(THIS_FOLDER, os.pardir, 'demo.docx')
    document = Document()
    table = document.add_table(rows=0, cols=7)
    lp = 1

    #for stopien, imie, nazwisko, data_wyjazdu, data_przyjazdu, miasto in queryset:
    for i in queryset:
        print(i)
        # formatowanie daty
        data = 'w dn. '
        if str(i.data_powrotu)[5:7] == str(i.data_wyjazdu)[5:7]:
            data += str(i.data_wyjazdu)[8:10] + ' - '
        else:
            data += str(i.data_wyjazdu)[8:10] + '.' + str(i.data_wyjazdu)[5:7] + ' - '
        data += str(i.data_powrotu)[8:10] + '.' + str(i.data_wyjazdu)[5:7] + '.' + str(i.data_wyjazdu)[0:4] + ' r.'
        # wpisywanie danych do tabeli
        komorki = table.add_row().cells
        komorki[0].text = str(lp) + ')'
        komorki[1].text = i.stopien
        komorki[2].text = i.imie
        komorki[3].text = str(i.nazwisko).upper()
        komorki[4].text = data
        komorki[5].text = 'do m.'
        komorki[6].text = i.miasto
        lp += 1
    #ustawianie parametrów dokumentu
    style = document.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(12)

    i=1
    for row in table.rows:
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
    return response