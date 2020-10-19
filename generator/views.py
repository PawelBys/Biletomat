import os
from datetime import date, timedelta
from time import strftime

from django.shortcuts import render
from django.http import HttpResponse
from django.utils.dateparse import parse_date

from .forms import BiletForm
from docxtpl import DocxTemplate

##### TEST #########

# ze zmiennej request zbiera się informacje, np kto jest zalogowany

def home_view(request, *args, **kwargs):

    return render(request, "home.html")

def test(request):
    doc = DocxTemplate("sample.docx")
    context = { 'chuj': request.user }
    doc.render(context)
    doc.save("generated_doc.docx")
    response = HttpResponse(open("generated_doc.docx", 'rb').read())
    response['Content-Type'] = 'text/plain'
    response['Content-Disposition'] = 'attachment; filename=pobrane.docx'
    return response



def generuj(request):
    form = BiletForm()
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    sample_pj = os.path.join(THIS_FOLDER, 'sample_pj.docx')
    sample_ur = os.path.join(THIS_FOLDER, 'sample_ur.docx')
    generated_doc = os.path.join(THIS_FOLDER, 'generated_doc.docx')
    if request.method == "POST":
        form = BiletForm(request.POST)
        if form.is_valid():
            if request.POST.get('typ') == 'pj':

                doc = DocxTemplate(open(sample_pj,"rb"))
            elif request.POST.get('typ') == 'ur':
                doc = DocxTemplate(open(sample_ur,"rb"))
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
                        'kwota':request.POST.get('kwota'),
                        'kwota_slownie':request.POST.get('kwota_slownie'),

                       }
            doc.render(context)
            doc.save(generated_doc)
            response = HttpResponse(open(generated_doc, 'rb').read())
            response['Content-Type'] = 'text/plain'
            response['Content-Disposition'] = 'attachment; filename=pobrane.docx'
            return response
    context = {
        "form": form
    }
    return render(request, "generate.html", context)



def panel(request, *args, **kwargs):
    context = {
        "zmienna": "abcdefg"
    }
    return render(request, "panel.html", context)
