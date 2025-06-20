from django import forms
from .models import Event, Ticket, EventCategory

class EventSearchForm(forms.Form):
    """Form per la ricerca degli eventi"""
    
    search = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Cerca eventi, luoghi, città...'
        })
    )
    
    category = forms.ModelChoiceField(
        queryset=EventCategory.objects.all(),
        required=False,
        empty_label='Tutte le categorie',
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    
    city = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Città'
        })
    )
    
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    SORT_CHOICES = [
        ('date', 'Data evento'),
        ('-date', 'Data evento (decrescente)'),
        ('price', 'Prezzo (crescente)'),
        ('-price', 'Prezzo (decrescente)'),
        ('title', 'Nome A-Z'),
        ('-title', 'Nome Z-A'),
    ]
    
    sort = forms.ChoiceField(
        choices=SORT_CHOICES,
        required=False,
        initial='date',
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    
    available_only = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        label='Solo eventi disponibili'
    )

class EventForm(forms.ModelForm):
    """Form per la creazione/modifica di eventi (admin)"""
    
    class Meta:
        model = Event
        fields = [
            'title', 'slug', 'description', 'category',
            'date', 'venue', 'address', 'city',
            'image', 'max_capacity', 'is_active'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Titolo dell\'evento'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'URL slug (auto-generato dal titolo)'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Descrizione dettagliata dell\'evento'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'venue': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome del luogo'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Indirizzo completo'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Città'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'max_capacity': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
    
    def clean_slug(self):
        """Valida che lo slug sia unico"""
        slug = self.cleaned_data.get('slug')
        if Event.objects.filter(slug=slug).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('Questo slug è già utilizzato.')
        return slug
    
    def clean_date(self):
        """Valida che la data non sia nel passato"""
        from django.utils import timezone
        date = self.cleaned_data.get('date')
        if date and date < timezone.now():
            raise forms.ValidationError('La data dell\'evento non può essere nel passato.')
        return date

class TicketForm(forms.ModelForm):
    """Form per la creazione/modifica di biglietti"""
    
    class Meta:
        model = Ticket
        fields = [
            'event', 'name', 'ticket_type', 'description',
            'price', 'quantity', 'max_per_order', 'is_active'
        ]
        widgets = {
            'event': forms.Select(attrs={
                'class': 'form-select'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome del biglietto'
            }),
            'ticket_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descrizione del biglietto'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'step': 0.01
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),
            'max_per_order': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 10
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
    
    def clean(self):
        """Validazione generale del form"""
        cleaned_data = super().clean()
        quantity = cleaned_data.get('quantity')
        sold_quantity = self.instance.sold_quantity if self.instance.pk else 0
        
        if quantity is not None and quantity < sold_quantity:
            raise forms.ValidationError(
                f'La quantità non può essere inferiore ai biglietti già venduti ({sold_quantity}).'
            )
        
        return cleaned_data