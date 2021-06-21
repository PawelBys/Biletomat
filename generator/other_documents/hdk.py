import os
from datetime import date, timedelta

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import formats
from docxtpl import DocxTemplate

from generator.date_format import get_date
from generator.forms import HdkForm


def generuj_wniosek_hdk(request):
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    sample_hdk = os.path.join(THIS_FOLDER, 'sample_hdk.docx')

    generated_hdk = os.path.join(THIS_FOLDER, 'generated_hdk.docx')

    form=HdkForm()
    if request.method == "POST":
        form = HdkForm(request.POST)
        if form.is_valid():

            data_poczatku = form.cleaned_data.get('data_poczatku')
            data_konca = form.cleaned_data.get('data_konca')
            data_urlopu = get_date(data_poczatku, data_konca)

            data_oddania =form.cleaned_data.get('data_oddania')
            miejscowosc =form.cleaned_data.get('miejscowosc')
            motywacja =form.cleaned_data.get('motywacja')
            zaleglosci =form.cleaned_data.get('zaleglosci')
            kary = form.cleaned_data.get('kary')
            typ_donacji = form.cleaned_data.get('typ_donacji')
            wielkosc_donacji = form.cleaned_data.get('wielkosc_donacji')
            zalacznik = form.cleaned_data.get('zalacznik')


            this_user = User.objects.get(id=request.user.id)
            stopien = this_user.userprofile.stopien
            imie = this_user.userprofile.imie
            nazwisko = this_user.userprofile.nazwisko.upper()
            wydzial = this_user.userprofile.wydzial
            pluton = this_user.userprofile.pluton
            grupa = this_user.userprofile.grupa


            context ={
                'stopien':stopien,
                'imie': imie,
                'nazwisko': nazwisko,
                'pluton': pluton,
                'wydzial':wydzial,
                'grupa':grupa,
                'data':formats.date_format(date.today(),'d.m.Y'),
                'data_urlopu':data_urlopu,
                'data_oddania':formats.date_format(data_oddania,'d.m.Y'),
                'miejscowosc':miejscowosc,
                "motywacja":motywacja,
                'zaleglosci':zaleglosci,
                'kary':kary,
                'typ_donacji':typ_donacji,
                'wielkosc_donacji':wielkosc_donacji,
                'zalacznik':zalacznik,

            }
            doc = DocxTemplate(open(sample_hdk, "rb"))
            doc.render(context)
            doc.save(generated_hdk)

            response = HttpResponse(open(generated_hdk, 'rb').read())
            response['Content-Type'] = 'text/plain'

            response['Content-Disposition'] = 'attachment; filename = wniosek_hdk.docx'

            return response

    context = {
        "form": form,
        'fontColor': os.getenv('FONT_COLOR'),
        'typ_wniosku': 'Wniosek o urlop HDK'
    }
    if not request.user.is_authenticated:
        return render(request, "no_permission.html")
    else:
        return render(request, "generate.html", context)

