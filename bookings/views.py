from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.db import transaction
from django.utils import timezone
from .models import Booking, BookingItem
from events.models import Event, Ticket
from .forms import BookingForm
import json

@login_required
def create_booking(request, slug):
    """Vista per creare una nuova prenotazione"""
    event = get_object_or_404(Event, slug=slug, is_active=True)
    
    # Verifica se l'evento è passato
    if event.is_past:
        messages.error(request, "Non è possibile prenotare biglietti per eventi passati.")
        return redirect('event_detail', slug=slug)
    
    # Verifica se ci sono biglietti disponibili
    if event.is_sold_out:
        messages.error(request, "Questo evento è sold out.")
        return redirect('event_detail', slug=slug)
    
    tickets = event.tickets.filter(is_active=True, quantity__gt=0)
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            # Recupera i dati del carrello
            cart_data = json.loads(request.POST.get('cart_data', '{}'))
            
            if not cart_data:
                messages.error(request, "Seleziona almeno un biglietto.")
                return redirect('create_booking', slug=slug)
            
            try:
                with transaction.atomic():
                    # Crea la prenotazione
                    booking = Booking.objects.create(
                        user=request.user,
                        event=event,
                        email=form.cleaned_data['email'],
                        phone_number=form.cleaned_data['phone_number'],
                        total_amount=0,
                        notes=form.cleaned_data.get('notes', '')
                    )
                    
                    total_amount = 0
                    
                    # Crea gli elementi della prenotazione
                    for ticket_id, quantity in cart_data.items():
                        ticket = Ticket.objects.get(id=ticket_id, event=event)
                        quantity = int(quantity)
                        
                        # Verifica disponibilità
                        if ticket.available_quantity < quantity:
                            raise ValueError(f"Quantità non disponibile per {ticket.name}")
                        
                        subtotal = ticket.price * quantity
                        total_amount += subtotal
                        
                        BookingItem.objects.create(
                            booking=booking,
                            ticket=ticket,
                            quantity=quantity,
                            price=ticket.price,
                            subtotal=subtotal
                        )
                    
                    # Aggiorna il totale
                    booking.total_amount = total_amount
                    booking.save()
                    
                    # Reindirizza alla pagina di conferma
                    return redirect('booking_confirm', booking_code=booking.booking_code)
                    
            except Exception as e:
                messages.error(request, f"Errore durante la prenotazione: {str(e)}")
                return redirect('create_booking', slug=slug)
    else:
        # Precompila con i dati dell'utente
        initial_data = {
            'email': request.user.email,
            'phone_number': getattr(request.user, 'phone_number', '')
        }
        form = BookingForm(initial=initial_data)
    
    context = {
        'event': event,
        'tickets': tickets,
        'form': form,
    }
    return render(request, 'bookings/booking_form.html', context)

@login_required
def booking_confirm(request, booking_code):
    """Vista per confermare la prenotazione"""
    booking = get_object_or_404(Booking, booking_code=booking_code, user=request.user)
    
    if booking.status != 'pending':
        messages.info(request, "Questa prenotazione è già stata processata.")
        return redirect('booking_detail', booking_code=booking_code)
    
    if request.method == 'POST':
        # Simula il pagamento
        if request.POST.get('action') == 'confirm':
            booking.confirm()
            messages.success(request, "Prenotazione confermata con successo!")
            return redirect('booking_success', booking_code=booking_code)
        elif request.POST.get('action') == 'cancel':
            booking.cancel()
            messages.info(request, "Prenotazione cancellata.")
            return redirect('my_bookings')
    
    context = {
        'booking': booking,
    }
    return render(request, 'bookings/booking_confirm.html', context)

@login_required
def booking_success(request, booking_code):
    """Vista per mostrare il successo della prenotazione"""
    booking = get_object_or_404(
        Booking, 
        booking_code=booking_code, 
        user=request.user,
        status='confirmed'
    )
    
    context = {
        'booking': booking,
    }
    return render(request, 'bookings/booking_success.html', context)

class MyBookingsView(LoginRequiredMixin, ListView):
    """Vista per le prenotazioni dell'utente"""
    model = Booking
    template_name = 'bookings/my_bookings.html'
    context_object_name = 'bookings'
    paginate_by = 10
    
    def get_queryset(self):
        return Booking.objects.filter(
            user=self.request.user
        ).select_related('event').prefetch_related('items__ticket').order_by('-created_at')

@login_required
def booking_detail(request, booking_code):
    """Vista per il dettaglio di una prenotazione"""
    booking = get_object_or_404(Booking, booking_code=booking_code, user=request.user)
    
    context = {
        'booking': booking,
    }
    return render(request, 'bookings/booking_detail.html', context)

@login_required
def cancel_booking(request, booking_code):
    """Vista per cancellare una prenotazione"""
    booking = get_object_or_404(Booking, booking_code=booking_code, user=request.user)
    
    if not booking.is_cancellable:
        messages.error(request, "Questa prenotazione non può essere cancellata.")
        return redirect('booking_detail', booking_code=booking_code)
    
    if request.method == 'POST':
        booking.cancel()
        messages.success(request, "Prenotazione cancellata con successo.")
        return redirect('my_bookings')
    
    context = {
        'booking': booking,
    }
    return render(request, 'bookings/cancel_booking.html', context)

# API View per verificare la disponibilità dei biglietti
@login_required
def check_ticket_availability(request, ticket_id):
    """API per verificare la disponibilità di un biglietto"""
    try:
        ticket = Ticket.objects.get(id=ticket_id)
        return JsonResponse({
            'available': ticket.available_quantity,
            'max_per_order': ticket.max_per_order,
            'price': float(ticket.price),
        })
    except Ticket.DoesNotExist:
        return JsonResponse({'error': 'Biglietto non trovato'}, status=404)