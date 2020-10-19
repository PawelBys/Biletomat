from datetime import date, timedelta

from django import forms
from django.forms import DateInput


class BiletForm(forms.Form):
    MONTHS = {
        1: ('styczeń'), 2: ('luty'), 3: ('marzec'), 4: ('kwiecień'),
        5: ('maj'), 6: ('czerwiec'), 7: ('lipiec'), 8: ('sierpień'),
        9: ('wrzesień'), 10: ('październik'), 11: ('listopad'), 12: ('grudzień')
    }
    PLUTONY = ((1, 1), (2, 2), (3, 3), (4, 4), (5, 5))
    MIESIACE = ( ('styczeń', 'styczeń'), ('luty', 'luty'), ('marzec', 'marzec'), ('kwiecień', 'kwiecień'), ('maj', 'maj'), ('czerwiec', 'czerwiec'), ('lipiec', 'lipiec'), ('sierpień', 'sierpień'), ('wrzesień', 'wrzesień'), ('październik', 'październik'), ('listopad', 'listopad'), ('grudzień', 'grudzień'))
    STOPNIE = ( ('szer. pchor.', 'szer. pchor.'), ('st. szer. pchor.', 'st. szer. pchor.'), ('kpr. pchor.', 'kpr. pchor.'), ('st. kpr. pchor.', 'st. kpr. pchor.'), ('plut. pchor.', 'plut. pchor.'), ('sierż. pchor.', 'sierż. pchor.'))
    TYP = (('przepustkę jednorazową', 'PJ'), ('urlop', 'Urlop'))
    TAM = (('', 'tam'), (' i z powrotem', 'tam i z powrotem'))
    POCIAGI = ("osobowym", "Osobowy"), ("pospiesznym", "TLK"), ("ekspresowym", "IC/EIC/EIP")
    AUTOBUSY = ("zwykłej", "Zwykły"), ("przyspieszonej", "Przyspieszony")

    typ = forms.CharField(widget=forms.Select(choices=TYP))
    imie_nazwisko = forms.CharField(max_length=50)
    stopien = forms.CharField(widget=forms.Select(choices=STOPNIE))
    adres = forms.CharField(max_length=100, initial='ul. Kolejowa 7/23, 01-476 Warszawa')
    pluton = forms.CharField(widget=forms.Select(choices=PLUTONY))
    data_wyjazdu = forms.DateField(widget=DateInput(), initial=date.today())
    data_powrotu = forms.DateField( widget=DateInput(), initial=date.today())
    tam_z_powrotem = forms.CharField(widget=forms.Select(choices=TAM), required=False)
    miasto = forms.CharField(max_length=30)
    miesiac = forms.CharField(widget=forms.Select(choices=MIESIACE))
    typ_pociagu = forms.MultipleChoiceField(choices=POCIAGI, widget=forms.CheckboxSelectMultiple, required=False)
    typ_autobusu = forms.MultipleChoiceField(choices=AUTOBUSY, widget=forms.CheckboxSelectMultiple, required=False)
    kwota = forms.DecimalField(decimal_places=2, max_digits=10)



