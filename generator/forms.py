from datetime import date, timedelta
#from importlib._common import _

from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import DateInput

from generator.models import UserProfile


class DateInput(forms.DateInput):
    input_type = 'date'


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
    TAM = (('', 'w jedną stronę'), (' i z powrotem', 'w dwie strony'))
    POCIAGI = ("osobowym", "Osobowy"), ("pospiesznym", "TLK"), ("ekspresowym", "IC/EIC/EIP")
    AUTOBUSY = ("zwykłej", "Zwykły"), ("przyspieszonej", "Przyspieszony")


    def clean(self):
        cleaned_data = self.cleaned_data
        end_date = cleaned_data.get('data_przyjazdu')
        start_date = cleaned_data.get('data_wyjazdu')
        if end_date and start_date:
            if end_date < start_date:
                self.add_error('data_przyjazdu', 'Event end date should not occur before start date.')
        return cleaned_data


    typ = forms.CharField(widget=forms.Select(choices=TYP, attrs={'class':'normal'}))
    # imie = forms.CharField(max_length=50, label="Imię", widget=forms.TextInput(attrs={'class':'normal'})  )
    # nazwisko = forms.CharField(max_length=50, label="Nazwisko", widget=forms.TextInput(attrs={'class':'normal'}))
    # stopien = forms.CharField(widget=forms.Select(choices=STOPNIE, attrs={'class':'normal'}), label="Stopień")
    # adres = forms.CharField(max_length=100, initial='', help_text="WZÓR: ul. Kolejowa 7/23, 01-476 Warszawa", widget=forms.TextInput(attrs={'class':'normal'}))
    # pluton = forms.CharField(widget=forms.Select(choices=PLUTONY, attrs={'class':'normal'}))
    #data_wyjazdu = forms.DateField(widget=DateInput(attrs={'class':'data'}), initial=date.today(), help_text="Data z blankietu (np. sobota, nie piątek)")
    #data_powrotu = forms.DateField( widget=DateInput(attrs={'class':'data'}), initial=date.today())
    data_wyjazdu = forms.DateField(widget=DateInput, initial=date.today(), label="Data rozpoczęcia PJ/urlopu", help_text="Data rozpoczęcia urlopu/PJ z blankietu, nie fizycznego wyjazdu (zazwyczaj wyjeżdża się dzień wcześniej)" )
    data_powrotu = forms.DateField(widget=DateInput, initial=date.today(), label="Data końca PJ/urlopu")
    tam_z_powrotem = forms.CharField(widget=forms.Select(choices=TAM, attrs={'class':'normal'}), required=False, label="W jedną / w dwie strony", )
    miasto = forms.CharField(max_length=30, label="Miasto podróży (z biletu)", widget=forms.TextInput(attrs={'class':'normal'}))
    miesiac = forms.CharField(widget=forms.Select(choices=MIESIACE, attrs={'class':'normal'}), label="Miesiąc", help_text="Miesiąc za jaki chcesz otrzymać należność")
    typ_pociagu = forms.MultipleChoiceField(choices=POCIAGI, widget=forms.CheckboxSelectMultiple(attrs={'class':'xxx'}), required=False, label="Typ pociągu")
    typ_autobusu = forms.MultipleChoiceField(choices=AUTOBUSY, widget=forms.CheckboxSelectMultiple(attrs={'class':'czekbox'}), required=False)
    kwota = forms.DecimalField(decimal_places=2, max_digits=10, label="Suma kwot z biletów", required=True, widget=forms.NumberInput(attrs={'class':'normal'}))
    zgoda = forms.BooleanField(help_text="Zgadzam się na przetwarzanie danych potrzebnych do sporządzenia rozkazu zgodnie z informacjami zawartymi w zakładce 'FAQ' w punkcie 10.")

class LoginForm(forms.Form):
    login = forms.CharField(max_length=50, label="Login", widget=forms.TextInput)
    password = forms.CharField(max_length=50, label="Hasło", widget=forms.PasswordInput)

class RegisterForm(UserCreationForm):
    STOPNIE = (
    ('szer. pchor.', 'szer. pchor.'), ('st. szer. pchor.', 'st. szer. pchor.'), ('kpr. pchor.', 'kpr. pchor.'),
    ('st. kpr. pchor.', 'st. kpr. pchor.'), ('plut. pchor.', 'plut. pchor.'), ('sierż. pchor.', 'sierż. pchor.'))
    PLUTONY = ((1, 1), (2, 2), (3, 3), (4, 4), (5, 5))
    WYDZIALY = ( ('WCY','WCY'),('WIG','WIG'),('WTC','WTC'),('WEL','WEL'),('WIM','WIM'),('WML','WML'),('WLO','WLO'),  )


    imie = forms.CharField(max_length=50, label="Imię", widget=forms.TextInput(attrs={'class': 'normal'}))
    nazwisko = forms.CharField(max_length=50, label="Nazwisko", widget=forms.TextInput(attrs={'class': 'normal'}))
    stopien = forms.CharField(widget=forms.Select(choices=STOPNIE, attrs={'class': 'normal'}), label="Stopień")
    adres = forms.CharField(max_length=100, initial='', help_text="WZÓR: ul. Kolejowa 7/23, 01-476 Warszawa",
                            widget=forms.TextInput(attrs={'class': 'normal'}))
    pluton = forms.CharField(widget=forms.Select(choices=PLUTONY, attrs={'class': 'normal'}))
    wydzial = forms.CharField(widget=forms.Select(choices=WYDZIALY, attrs={'class': 'normal'}), label="Wydział")
    grupa = forms.CharField(max_length=50, label="Grupa", widget=forms.TextInput(attrs={'class': 'normal'}))


    class Meta:
        model = User
        fields = ("username",)




    def save(self, commit=True):
        if not commit:
            raise NotImplementedError("Can't create User and UserProfile without database save")
        imie = self.cleaned_data['imie']
        nazwisko = self.cleaned_data['nazwisko']
        stopien = self.cleaned_data['stopien']
        adres = self.cleaned_data['adres']
        pluton = self.cleaned_data['pluton']
        wydzial = self.cleaned_data['wydzial']
        grupa = self.cleaned_data['grupa']

        user = super(RegisterForm, self).save(commit=True)
        userProfile = UserProfile.objects.create(
            user=user,
            imie=imie,
            nazwisko = nazwisko,
            stopien = stopien,
            adres = adres,
            pluton = pluton,
            wydzial = wydzial,
            grupa = grupa
        )

        userProfile.save()
        return user

class HdkForm(forms.Form):
    data_poczatku = forms.DateField(widget=DateInput, initial=date.today(), label="Data początku urlopu", required=True)
    data_konca = forms.DateField(widget=DateInput, initial=date.today(), label="Data końca urlopu", required=True)
    data_oddania = forms.DateField(widget=DateInput, initial=date.today(), label="Data oddania krwi", required=True)
    miejscowosc = forms.CharField(max_length=30, label="Miasto",
                             widget=forms.TextInput(attrs={'class': 'normal'}), required=True,
                                  help_text="Na urlop udam się do miejscowości:")
    motywacja = forms.CharField(max_length=200, label="Motywacja",
                                 widget=forms.TextInput(attrs={'class': 'normal'}),
                                 help_text="Dokończ zdanie (bez kropki na końcu)",
                                initial="Wniosek swój motywuję ", required=True)
    zaleglosci = forms.CharField(max_length=200, label="Zaległości",
                                  widget=forms.TextInput(attrs={'class': 'normal'}),
                                  help_text="nie posiadam zaległości w nauce/posiadam zaległości:... (wymień)(bez kropki na końcu)",
                                initial="nie posiadam zaległości w nauce", required=True)
    kary = forms.CharField(max_length=200, label="Kary dyscyplinarne",
                                  widget=forms.TextInput(attrs={'class': 'normal'}),
                                   help_text="nie posiadam kar dyscyplinarnych/posiadam kary:...(wymień)(bez kropki na końcu)",
                                   initial="nie posiadam kar dyscyplinarnych", required=True)

class PjForm(forms.Form):
    data_poczatku = forms.DateField(widget=DateInput, initial=date.today(), label="Data początku pj", required=True)
    data_konca = forms.DateField(widget=DateInput, initial=date.today(), label="Data końca pj", required=True)
    miejscowosc = forms.CharField(max_length=30, label="Miasto",
                             widget=forms.TextInput(attrs={'class': 'normal'}), required=True,
                                  help_text="Na przepustkę udam się do miejscowości:")
    motywacja = forms.CharField(max_length=200, label="Motywacja",
                                 widget=forms.TextInput(attrs={'class': 'normal'}),
                                 help_text="Dokończ zdanie (bez kropki na końcu)",
                                initial="Wniosek swój motywuję ", required=True)
    zaleglosci = forms.CharField(max_length=200, label="Zaległości",
                                  widget=forms.TextInput(attrs={'class': 'normal'}),
                                  help_text="nie posiadam zaległości w nauce/posiadam zaległości:... (wymień)(bez kropki na końcu)",
                                initial="nie posiadam zaległości w nauce", required=True)
    kary = forms.CharField(max_length=200, label="Kary dyscyplinarne",
                                  widget=forms.TextInput(attrs={'class': 'normal'}),
                                   help_text="nie posiadam kar dyscyplinarnych/posiadam kary:...(wymień)(bez kropki na końcu)",
                                   initial="nie posiadam kar dyscyplinarnych", required=True)