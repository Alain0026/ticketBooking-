from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Q, Min
from .models import Event, Ticket
from .serializers import (
    EventListSerializer, 
    EventDetailSerializer, 
    TicketSerializer
)

class EventViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API ViewSet per gli eventi.
    Permette solo operazioni di lettura (GET).
    """
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'venue', 'city']
    ordering_fields = ['date', 'title', 'min_price']
    ordering = ['date']
    
    def get_queryset(self):
        queryset = Event.objects.filter(
            is_active=True,
            date__gte=timezone.now()
        ).select_related('category').prefetch_related('tickets')
        
        # Aggiungi annotazione per min_price
        queryset = queryset.annotate(min_price=Min('tickets__price'))
        
        # Filtro per categoria
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category__slug=category)
        
        # Filtro per città
        city = self.request.query_params.get('city', None)
        if city:
            queryset = queryset.filter(city__icontains=city)
        
        # Filtro per disponibilità
        available_only = self.request.query_params.get('available_only', None)
        if available_only and available_only.lower() == 'true':
            queryset = queryset.exclude(
                id__in=[e.id for e in queryset if e.is_sold_out]
            )
        
        # Limite risultati
        limit = self.request.query_params.get('limit', None)
        if limit:
            try:
                limit = int(limit)
                queryset = queryset[:limit]
            except ValueError:
                pass
        
        return queryset
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return EventDetailSerializer
        return EventListSerializer
    
    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Restituisce i prossimi 10 eventi"""
        events = self.get_queryset()[:10]
        serializer = EventListSerializer(events, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Restituisce eventi in evidenza (con più biglietti venduti)"""
        events = Event.objects.filter(
            is_active=True,
            date__gte=timezone.now()
        ).select_related('category').prefetch_related('tickets')
        
        # Ordina per numero di biglietti venduti
        events = sorted(
            events, 
            key=lambda e: sum(t.sold_quantity for t in e.tickets.all()),
            reverse=True
        )[:6]
        
        serializer = EventListSerializer(events, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def tickets(self, request, pk=None):
        """Restituisce i biglietti disponibili per un evento"""
        event = self.get_object()
        tickets = event.tickets.filter(is_active=True)
        serializer = TicketSerializer(tickets, many=True)
        return Response(serializer.data)

class TicketViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API ViewSet per i biglietti.
    Permette solo operazioni di lettura (GET).
    """
    queryset = Ticket.objects.filter(is_active=True)
    serializer_class = TicketSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtro per evento
        event_id = self.request.query_params.get('event', None)
        if event_id:
            queryset = queryset.filter(event_id=event_id)
        
        # Filtro per tipo
        ticket_type = self.request.query_params.get('type', None)
        if ticket_type:
            queryset = queryset.filter(ticket_type=ticket_type)
        
        # Solo biglietti disponibili
        available_only = self.request.query_params.get('available_only', None)
        if available_only and available_only.lower() == 'true':
            queryset = queryset.filter(quantity__gt=0)
        
        return queryset