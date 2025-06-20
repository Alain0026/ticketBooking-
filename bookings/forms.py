from django import forms
from django.core.validators import RegexValidator
from .models import Booking

class BookingForm(forms.Form):
    """Form per la creazione di una prenotazione"""
    
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'La tua email',
            'required': True
        })
    )
    
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Inserisci un numero di telefono valido."
    )
    
    phone_number = forms.CharField(
        label='Numero di telefono',
        validators=[phone_regex],
        max_length=17,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Il tuo numero di telefono',
            'required': True
        })
    )
    
    notes = forms.CharField(
        label='Note aggiuntive (opzionale)',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Eventuali richieste speciali o note...'
        })
    )
    
    terms_accepted = forms.BooleanField(
        label='Accetto i termini e le condizioni',
        required=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
            'required': True
        })
    )

class PaymentForm(forms.Form):
    """Form simulato per il pagamento"""
    
    card_number = forms.CharField(
        label='Numero Carta',
        max_length=16,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '1234 5678 9012 3456',
            'pattern': '[0-9]{16}',
            'maxlength': '16'
        })
    )
    
    card_holder = forms.CharField(
        label='Intestatario Carta',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nome Cognome'
        })
    )
    
    expiry_month = forms.ChoiceField(
        label='Mese Scadenza',
        choices=[(str(i).zfill(2), str(i).zfill(2)) for i in range(1, 13)],
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    
    expiry_year = forms.ChoiceField(
        label='Anno Scadenza',
        choices=[(str(i), str(i)) for i in range(2024, 2035)],
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    
    cvv = forms.CharField(
        label='CVV',
        max_length=3,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '123',
            'pattern': '[0-9]{3}',
            'maxlength': '3'
        })
    )