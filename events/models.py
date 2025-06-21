from django.db import models
from django.urls import reverse
from django.utils import timezone
from cloudinary.models import CloudinaryField

class EventCategory(models.Model):
    """Categoria degli eventi"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    
    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorie'
        
    def __str__(self):
        return self.name

class Event(models.Model):
    """Modello per gli eventi"""
    title = models.CharField(max_length=200, verbose_name='Titolo')
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(verbose_name='Descrizione')
    category = models.ForeignKey(EventCategory, on_delete=models.SET_NULL, null=True, related_name='events')
    
    # Informazioni sull'evento
    date = models.DateTimeField(verbose_name='Data e ora')
    venue = models.CharField(max_length=200, verbose_name='Luogo')
    address = models.TextField(verbose_name='Indirizzo')
    city = models.CharField(max_length=100, verbose_name='Città')
    
    # Immagine - compatibile con Cloudinary
    image = models.ImageField(
        upload_to='events/', 
        blank=True, 
        null=True,
        help_text='Immagine dell\'evento (sarà caricata su Cloudinary in produzione)'
    )
    
    # Prezzi e disponibilità
    max_capacity = models.IntegerField(verbose_name='Capienza massima')
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True, verbose_name='Attivo')
    
    class Meta:
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventi'
        ordering = ['date']
        
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('event_detail', kwargs={'slug': self.slug})
    
    @property
    def is_past(self):
        return self.date < timezone.now()
    
    @property
    def is_sold_out(self):
        total_sold = sum(ticket.sold_quantity for ticket in self.tickets.all())
        total_capacity = sum(ticket.quantity for ticket in self.tickets.all())
        return total_sold >= total_capacity
    
    @property
    def available_tickets(self):
        return sum(ticket.available_quantity for ticket in self.tickets.all())
    
    @property
    def min_price(self):
        prices = [ticket.price for ticket in self.tickets.filter(is_active=True)]
        return min(prices) if prices else 0

class Ticket(models.Model):
    """Modello per i tipi di biglietti"""
    TICKET_TYPES = [
        ('standard', 'Standard'),
        ('vip', 'VIP'),
        ('premium', 'Premium'),
        ('student', 'Studente'),
        ('group', 'Gruppo'),
    ]
    
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='tickets')
    name = models.CharField(max_length=100, verbose_name='Nome biglietto')
    ticket_type = models.CharField(max_length=20, choices=TICKET_TYPES, default='standard')
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Prezzo')
    quantity = models.IntegerField(verbose_name='Quantità disponibile')
    sold_quantity = models.IntegerField(default=0, verbose_name='Quantità venduta')
    
    # Limitazioni
    max_per_order = models.IntegerField(default=10, verbose_name='Max per ordine')
    
    # Metadata
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Biglietto'
        verbose_name_plural = 'Biglietti'
        unique_together = ['event', 'name']
        
    def __str__(self):
        return f"{self.name} - {self.event.title}"
    
    @property
    def available_quantity(self):
        return self.quantity - self.sold_quantity
    
    @property
    def is_available(self):
        return self.available_quantity > 0 and self.is_active