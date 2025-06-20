from django.db import models
from django.conf import settings
from django.utils import timezone
from events.models import Event, Ticket
import uuid

class Booking(models.Model):
    """Modello per le prenotazioni"""
    STATUS_CHOICES = [
        ('pending', 'In attesa'),
        ('confirmed', 'Confermata'),
        ('cancelled', 'Cancellata'),
        ('completed', 'Completata'),
    ]
    
    # Identificativo unico
    booking_code = models.CharField(max_length=20, unique=True, editable=False)
    
    # Relazioni
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='bookings')
    
    # Informazioni prenotazione
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Informazioni di contatto
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    
    # Note aggiuntive
    notes = models.TextField(blank=True, null=True)
    
    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    confirmed_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        verbose_name = 'Prenotazione'
        verbose_name_plural = 'Prenotazioni'
        ordering = ['-created_at']
        
    def __str__(self):
        return f"Prenotazione {self.booking_code} - {self.user.username}"
    
    def save(self, *args, **kwargs):
        if not self.booking_code:
            self.booking_code = self.generate_booking_code()
        super().save(*args, **kwargs)
    
    def generate_booking_code(self):
        """Genera un codice prenotazione univoco"""
        code = f"BK{uuid.uuid4().hex[:8].upper()}"
        while Booking.objects.filter(booking_code=code).exists():
            code = f"BK{uuid.uuid4().hex[:8].upper()}"
        return code
    
    def confirm(self):
        """Conferma la prenotazione"""
        self.status = 'confirmed'
        self.confirmed_at = timezone.now()
        self.save()
        
        # Aggiorna le quantità vendute dei biglietti
        for item in self.items.all():
            item.ticket.sold_quantity += item.quantity
            item.ticket.save()
    
    def cancel(self):
        """Cancella la prenotazione"""
        if self.status == 'confirmed':
            # Ripristina le quantità dei biglietti
            for item in self.items.all():
                item.ticket.sold_quantity -= item.quantity
                item.ticket.save()
        
        self.status = 'cancelled'
        self.save()
    
    @property
    def is_editable(self):
        """Verifica se la prenotazione può essere modificata"""
        return self.status == 'pending' and not self.event.is_past
    
    @property
    def is_cancellable(self):
        """Verifica se la prenotazione può essere cancellata"""
        return self.status in ['pending', 'confirmed'] and not self.event.is_past

class BookingItem(models.Model):
    """Dettagli dei biglietti in una prenotazione"""
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='items')
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        verbose_name = 'Elemento prenotazione'
        verbose_name_plural = 'Elementi prenotazione'
        
    def __str__(self):
        return f"{self.quantity}x {self.ticket.name}"
    
    def save(self, *args, **kwargs):
        """Calcola automaticamente il subtotale prima di salvare"""
        self.subtotal = self.price * self.quantity
        super().save(*args, **kwargs)