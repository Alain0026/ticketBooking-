from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Booking
from .serializers import (
    BookingListSerializer,
    BookingDetailSerializer,
    CreateBookingSerializer,
    BookingStatusSerializer
)

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permesso personalizzato per permettere solo al proprietario
    di modificare la propria prenotazione
    """
    def has_object_permission(self, request, view, obj):
        # Lettura permessa a tutti gli autenticati
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        # Scrittura permessa solo al proprietario
        return obj.user == request.user

class BookingViewSet(viewsets.ModelViewSet):
    """
    API ViewSet per le prenotazioni.
    
    list: Restituisce le prenotazioni dell'utente autenticato
    create: Crea una nuova prenotazione
    retrieve: Mostra i dettagli di una prenotazione
    update/partial_update: Aggiorna una prenotazione (solo se in stato pending)
    destroy: Cancella una prenotazione (solo se cancellabile)
    """
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    
    def get_queryset(self):
        """Restituisce solo le prenotazioni dell'utente autenticato"""
        return Booking.objects.filter(
            user=self.request.user
        ).select_related('event').prefetch_related('items__ticket')
    
    def get_serializer_class(self):
        """Usa serializer diversi per azioni diverse"""
        if self.action == 'create':
            return CreateBookingSerializer
        elif self.action == 'retrieve':
            return BookingDetailSerializer
        elif self.action in ['confirm', 'cancel']:
            return BookingStatusSerializer
        return BookingListSerializer
    
    def create(self, request, *args, **kwargs):
        """Crea una nuova prenotazione"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        booking = serializer.save()
        
        # Restituisci i dettagli della prenotazione creata
        detail_serializer = BookingDetailSerializer(booking)
        return Response(
            detail_serializer.data, 
            status=status.HTTP_201_CREATED
        )
    
    def update(self, request, *args, **kwargs):
        """Aggiorna una prenotazione (solo se in stato pending)"""
        booking = self.get_object()
        
        if not booking.is_editable:
            return Response(
                {"error": "Questa prenotazione non può essere modificata."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        """Cancella una prenotazione"""
        booking = self.get_object()
        
        if not booking.is_cancellable:
            return Response(
                {"error": "Questa prenotazione non può essere cancellata."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        booking.cancel()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        """Conferma una prenotazione e processa il pagamento"""
        booking = self.get_object()
        serializer = self.get_serializer(
            data={'action': 'confirm'},
            context={'booking': booking}
        )
        serializer.is_valid(raise_exception=True)
        
        # Conferma la prenotazione
        booking.confirm()
        
        # Restituisci i dettagli aggiornati
        detail_serializer = BookingDetailSerializer(booking)
        return Response(detail_serializer.data)
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancella una prenotazione"""
        booking = self.get_object()
        serializer = self.get_serializer(
            data={'action': 'cancel'},
            context={'booking': booking}
        )
        serializer.is_valid(raise_exception=True)
        
        # Cancella la prenotazione
        booking.cancel()
        
        # Restituisci i dettagli aggiornati
        detail_serializer = BookingDetailSerializer(booking)
        return Response(detail_serializer.data)
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Restituisce statistiche sulle prenotazioni dell'utente"""
        bookings = self.get_queryset()
        
        stats = {
            'total_bookings': bookings.count(),
            'confirmed_bookings': bookings.filter(status='confirmed').count(),
            'pending_bookings': bookings.filter(status='pending').count(),
            'cancelled_bookings': bookings.filter(status='cancelled').count(),
            'total_spent': sum(
                b.total_amount for b in bookings.filter(status='confirmed')
            ),
            'upcoming_events': bookings.filter(
                status='confirmed',
                event__date__gte=timezone.now()
            ).count(),
        }
        
        return Response(stats)
    
    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Restituisce le prenotazioni per eventi futuri"""
        bookings = self.get_queryset().filter(
            status='confirmed',
            event__date__gte=timezone.now()
        ).order_by('event__date')
        
        page = self.paginate_queryset(bookings)
        if page is not None:
            serializer = BookingListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = BookingListSerializer(bookings, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def past(self, request):
        """Restituisce le prenotazioni per eventi passati"""
        bookings = self.get_queryset().filter(
            status='confirmed',
            event__date__lt=timezone.now()
        ).order_by('-event__date')
        
        page = self.paginate_queryset(bookings)
        if page is not None:
            serializer = BookingListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = BookingListSerializer(bookings, many=True)
        return Response(serializer.data)