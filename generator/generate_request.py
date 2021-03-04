import os
from datetime import timedelta, date

from django.utils.dateparse import parse_date

from generator.models import Dane

from docxtpl import DocxTemplate
from generator.kwotaslownie import kwotaslownie

# ze zmiennej request zbiera się informacje, np kto jest zalogowany

from .maketable import switch_stopien

def generuj_ext(request, form, generated_doc):
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    sample_pj = os.path.join(THIS_FOLDER, 'sample_pj.docx')
    sample_ur = os.path.join(THIS_FOLDER, 'sample_ur.docx')

    typ_pociagu = form.cleaned_data.get('typ_pociagu')
    typ_autobusu = form.cleaned_data.get('typ_autobusu')
    temp_typ_srodka = ""
    srodek = ""

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
        doc = DocxTemplate(open(sample_pj, "rb"))
    elif request.POST.get('typ') == 'urlop':
        doc = DocxTemplate(open(sample_ur, "rb"))
    data_wyjazdu = request.POST.get('data_wyjazdu')
    data_powrotu = request.POST.get('data_powrotu')
    miasto = request.POST.get('miasto')
    stopien = request.POST.get('stopien')
    imie = request.POST.get('imie')
    nazwisko = request.POST.get('nazwisko')
    typ = request.POST.get('typ')
    miesiac = request.POST.get('miesiac')

    # przypisanie id stopnia do stopnia
    wyliczony_stopien = switch_stopien(stopien)

    # liczenie nr rozkazu batalionowego
    wstepna_data = parse_date(request.POST.get('data_wyjazdu'))
    # wstepna_data = parse_date(date(data_wyjazdu.year))
    data_rozkazu = '.............'
    nr_rozkazu = '.............'
    if wstepna_data.weekday() == 5 or wstepna_data.weekday() == 4:
        if wstepna_data.weekday() == 5:
            data_rozkazu = wstepna_data - timedelta(days=2)
        else:
            data_rozkazu = wstepna_data - timedelta(days=1)

        # dnia 24.09.2020 był nr rozkazu 76
        # odejmij datę wyjazdu od 24.09, uzyskane dni pocziel na 7 i pomnóż razy 2 - spodziewana liczba wydanych rozkazow
        nr_rozkazu = 0
        if(data_rozkazu.year == 2021):
            nr_rozkazu = int(1 + (((data_rozkazu - date(2021, 1, 5)).days + 1) / 7) * 2)
        if(data_rozkazu.year == 2020):
            nr_rozkazu = int(76 + (((data_rozkazu - date(2020, 9, 24)).days + 1) / 7) * 2)

    context = {'stopien': request.POST.get('stopien'),
               'imie': request.POST.get('imie'),
               'nazwisko': request.POST.get('nazwisko'),
               'adres': request.POST.get('adres'),
               'pluton': request.POST.get('pluton'),
               'data_przed': parse_date(request.POST.get('data_wyjazdu')) - timedelta(days=1),
               'data_wyjazdu': request.POST.get('data_wyjazdu'),
               'data_powrotu': request.POST.get('data_powrotu'),
               'miesiac': request.POST.get('miesiac'),
               'miejscowosc': request.POST.get('miasto'),
               'kwota': kwota,
               'kwota_slownie': kwotaslownie(kwota, 1),
               'typ': request.POST.get('typ'),
               'typ_srodka': typ_srodka,
               'srodek': srodek,
               'powrot': request.POST.get('tam_z_powrotem'),
               'data_rozkazu': data_rozkazu,
               'nr_rozkazu': nr_rozkazu,

               }
    nazwisko = nazwisko.upper()
    # tworzenie obiektu bazy danych
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
            dana.miesiac = miesiac
            dana.stopien_id = wyliczony_stopien
            dana.nr_rozkazu = nr_rozkazu
            dana.save()
        else:
            rekord = Dane(data_wyjazdu=data_wyjazdu, data_powrotu=data_powrotu, miasto=miasto, stopien=stopien,
                          imie=imie, nazwisko=nazwisko, typ=typ, transport=srodek, miesiac=miesiac,
                          stopien_id=wyliczony_stopien, nr_rozkazu=nr_rozkazu)
            rekord.save()
    else:
        q = Dane.objects.filter(imie=imie, nazwisko=nazwisko, typ=typ, data_wyjazdu=data_wyjazdu,
                                data_powrotu=data_powrotu)
        if q.exists():  # jeśli obiekt istnieje, zaktualizuj jego dane
            dana = Dane.objects.get(imie=imie, nazwisko=nazwisko, typ=typ, data_wyjazdu=data_wyjazdu,
                                    data_powrotu=data_powrotu)
            dana.data_wyjazdu = data_wyjazdu
            dana.data_powrotu = data_powrotu
            dana.miasto = miasto
            dana.stopien = stopien
            dana.typ = typ
            dana.transport = srodek
            dana.stopien_id = wyliczony_stopien
            dana.nr_rozkazu = nr_rozkazu

            dana.save()
        else:
            rekord = Dane(data_wyjazdu=data_wyjazdu, data_powrotu=data_powrotu, miasto=miasto, stopien=stopien,
                          imie=imie, nazwisko=nazwisko, typ=typ, transport=srodek, stopien_id=wyliczony_stopien,
                          nr_rozkazu=nr_rozkazu)
            rekord.save()
    doc.render(context)
    doc.save(generated_doc)
