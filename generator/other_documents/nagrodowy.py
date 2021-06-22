import os
from datetime import date, timedelta

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import formats
from docxtpl import DocxTemplate

from generator.date_format import get_date
from generator.forms import HdkForm, NagrodowyForm


def generuj_wniosek_nagrodowy(request):
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    sample_nagrodowy = os.path.join(THIS_FOLDER, 'sample_nagrodowy.docx')

    generated_nagrodowy = os.path.join(THIS_FOLDER, 'generated_nagrodowy.docx')

    form=NagrodowyForm()
    if request.method == "POST":
        form = NagrodowyForm(request.POST)
        if form.is_valid():

            data_poczatku = form.cleaned_data.get('data_poczatku')
            data_konca = form.cleaned_data.get('data_konca')
            data_urlopu = get_date(data_poczatku, data_konca)

            data_rozkazu =form.cleaned_data.get('data_rozkazu')
            nr_rozkazu =form.cleaned_data.get('nr_rozkazu')
            miejscowosc =form.cleaned_data.get('miejscowosc')
            motywacja =form.cleaned_data.get('motywacja')
            zaleglosci =form.cleaned_data.get('zaleglosci')
            kary =form.cleaned_data.get('kary')



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
                'data':str(date.today()),
                'data_urlopu':data_urlopu,
                'data_rozkazu':formats.date_format(data_rozkazu,"dd.mm.yyyy"),
                'nr_rozkazu':nr_rozkazu,
                'miejscowosc':miejscowosc,
                "motywacja":motywacja,
                'zaleglosci':zaleglosci,
                'kary':kary,

            }
            doc = DocxTemplate(open(sample_nagrodowy, "rb"))
            doc.render(context)
            doc.save(generated_nagrodowy)

            response = HttpResponse(open(generated_nagrodowy, 'rb').read())
            response['Content-Type'] = 'text/plain'

            response['Content-Disposition'] = 'attachment; filename = wniosek_nagrodowy.docx'

            return response

    context = {
        "form": form,
        'fontColor': os.getenv('FONT_COLOR'),
        'typ_wniosku': 'Wniosek nagrodowy'
    }
    if not request.user.is_authenticated:
        return render(request, "no_permission.html")
    else:
        return render(request, "generate.html", context)

