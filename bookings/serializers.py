from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Booking, BookingItem
from events.serializers import EventListSerializer, TicketSerializer

User = get_user_model()

class BookingItemSerializer(serializers.ModelSerializer):
    """Serializer per gli elementi di una prenotazione"""
    ticket = TicketSerializer(read_only=True)
    ticket_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = BookingItem
        fields = ['id', 'ticket', 'ticket_id', 'quantity', 'price', 'subtotal']
        read_only_fields = ['price', 'subtotal']

class BookingListSerializer(serializers.ModelSerializer):
    """Serializer per la lista delle prenotazioni"""
    event = EventListSerializer(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    is_editable = serializers.ReadOnlyField()
    is_cancellable = serializers.ReadOnlyField()
    
    class Meta:
        model = Booking
        fields = [
            'id', 'booking_code', 'event', 'status', 'status_display',
            'total_amount', 'created_at', 'is_editable', 'is_cancellable'
        ]
        read_only_fields = ['booking_code', 'total_amount', 'created_at']

class BookingDetailSerializer(serializers.ModelSerializer):
    """Serializer per il dettaglio di una prenotazione"""
    event = EventListSerializer(read_only=True)
    items = BookingItemSerializer(many=True, read_only=True)
    user = serializers.StringRelatedField(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    is_editable = serializers.ReadOnlyField()
    is_cancellable = serializers.ReadOnlyField()
    
    class Meta:
        model = Booking
        fields = [
            'id', 'booking_code', 'user', 'event', 'items', 
            'status', 'status_display', 'total_amount',
            'email', 'phone_number', 'notes',
            'created_at', 'updated_at', 'confirmed_at',
            'is_editable', 'is_cancellable'
        ]
        read_only_fields = [
            'booking_code', 'user', 'total_amount', 
            'created_at', 'updated_at', 'confirmed_at'
        ]

class CreateBookingSerializer(serializers.ModelSerializer):
    """Serializer per creare una nuova prenotazione"""
    items = BookingItemSerializer(many=True)
    event_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Booking
        fields = ['event_id', 'email', 'phone_number', 'notes', 'items']
    
    def validate_items(self, value):
        """Valida che ci sia almeno un biglietto"""
        if not value:
            raise serializers.ValidationError("Devi selezionare almeno un biglietto.")
        return value
    
    def validate(self, data):
        """Validazione generale della prenotazione"""
        from events.models import Event, Ticket
        
        # Verifica che l'evento esista e sia attivo
        try:
            event = Event.objects.get(id=data['event_id'], is_active=True)
        except Event.DoesNotExist:
            raise serializers.ValidationError("Evento non trovato o non disponibile.")
        
        # Verifica che l'evento non sia passato
        if event.is_past:
            raise serializers.ValidationError("Non puoi prenotare biglietti per eventi passati.")
        
        # Verifica disponibilità biglietti
        for item_data in data['items']:
            try:
                ticket = Ticket.objects.get(
                    id=item_data['ticket_id'], 
                    event=event,
                    is_active=True
                )
            except Ticket.DoesNotExist:
                raise serializers.ValidationError(f"Biglietto non valido.")
            
            if ticket.available_quantity < item_data['quantity']:
                raise serializers.ValidationError(
                    f"Quantità non disponibile per {ticket.name}. "
                    f"Disponibili: {ticket.available_quantity}"
                )
            
            if item_data['quantity'] > ticket.max_per_order:
                raise serializers.ValidationError(
                    f"Puoi ordinare massimo {ticket.max_per_order} "
                    f"biglietti {ticket.name} per ordine."
                )
        
        return data
    
    def create(self, validated_data):
        """Crea la prenotazione con tutti gli elementi"""
        from django.db import transaction
        from events.models import Event, Ticket
        
        items_data = validated_data.pop('items')
        event_id = validated_data.pop('event_id')
        
        with transaction.atomic():
            # Crea la prenotazione
            booking = Booking.objects.create(
                event_id=event_id,
                user=self.context['request'].user,
                **validated_data
            )
            
            total_amount = 0
            
            # Crea gli elementi della prenotazione
            for item_data in items_data:
                ticket = Ticket.objects.get(id=item_data['ticket_id'])
                quantity = item_data['quantity']
                subtotal = ticket.price * quantity
                
                BookingItem.objects.create(
                    booking=booking,
                    ticket=ticket,
                    quantity=quantity,
                    price=ticket.price,
                    subtotal=subtotal
                )
                
                total_amount += subtotal
            
            # Aggiorna il totale
            booking.total_amount = total_amount
            booking.save()
            
            return booking

class BookingStatusSerializer(serializers.Serializer):
    """Serializer per aggiornare lo stato di una prenotazione"""
    action = serializers.ChoiceField(choices=['confirm', 'cancel'])
    
    def validate(self, data):
        booking = self.context.get('booking')
        
        if data['action'] == 'confirm' and booking.status != 'pending':
            raise serializers.ValidationError("Solo le prenotazioni in attesa possono essere confermate.")
        
        if data['action'] == 'cancel' and not booking.is_cancellable:
            raise serializers.ValidationError("Questa prenotazione non può essere cancellata.")
        
        return data