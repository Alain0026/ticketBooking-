from rest_framework import serializers
from .models import Event, EventCategory, Ticket

class EventCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EventCategory
        fields = ['id', 'name', 'slug']

class TicketSerializer(serializers.ModelSerializer):
    available_quantity = serializers.ReadOnlyField()
    is_available = serializers.ReadOnlyField()
    
    class Meta:
        model = Ticket
        fields = [
            'id', 'name', 'ticket_type', 'description', 
            'price', 'quantity', 'sold_quantity', 
            'available_quantity', 'is_available', 
            'max_per_order'
        ]

class EventListSerializer(serializers.ModelSerializer):
    category = EventCategorySerializer(read_only=True)
    min_price = serializers.ReadOnlyField()
    is_sold_out = serializers.ReadOnlyField()
    available_tickets = serializers.ReadOnlyField()
    
    class Meta:
        model = Event
        fields = [
            'id', 'title', 'slug', 'category', 'date', 
            'venue', 'city', 'image', 'min_price', 
            'is_sold_out', 'available_tickets'
        ]

class EventDetailSerializer(serializers.ModelSerializer):
    category = EventCategorySerializer(read_only=True)
    tickets = TicketSerializer(many=True, read_only=True)
    is_past = serializers.ReadOnlyField()
    is_sold_out = serializers.ReadOnlyField()
    available_tickets = serializers.ReadOnlyField()
    min_price = serializers.ReadOnlyField()
    
    class Meta:
        model = Event
        fields = [
            'id', 'title', 'slug', 'description', 'category',
            'date', 'venue', 'address', 'city', 'image',
            'max_capacity', 'tickets', 'is_past', 'is_sold_out',
            'available_tickets', 'min_price', 'created_at', 'updated_at'
        ]