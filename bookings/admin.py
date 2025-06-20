from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Booking, BookingItem

class BookingItemInline(admin.TabularInline):
    """Inline per visualizzare i biglietti di una prenotazione"""
    model = BookingItem
    extra = 0
    readonly_fields = ['ticket', 'quantity', 'price', 'subtotal']
    can_delete = False
    
    def has_add_permission(self, request, obj=None):
        return False

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    """Admin per le prenotazioni"""
    list_display = [
        'booking_code', 'user_link', 'event_link', 
        'status_badge', 'total_amount', 'created_at'
    ]
    list_filter = ['status', 'created_at', 'event__category']
    search_fields = ['booking_code', 'user__username', 'user__email', 'event__title']
    date_hierarchy = 'created_at'
    readonly_fields = [
        'booking_code', 'user', 'event', 'total_amount', 
        'created_at', 'updated_at', 'confirmed_at'
    ]
    inlines = [BookingItemInline]
    
    fieldsets = (
        ('Informazioni Prenotazione', {
            'fields': ('booking_code', 'user', 'event', 'status')
        }),
        ('Dettagli Contatto', {
            'fields': ('email', 'phone_number', 'notes')
        }),
        ('Informazioni Pagamento', {
            'fields': ('total_amount',)
        }),
        ('Date', {
            'fields': ('created_at', 'updated_at', 'confirmed_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['confirm_bookings', 'cancel_bookings']
    
    def user_link(self, obj):
        """Link all'utente"""
        url = reverse('admin:accounts_customuser_change', args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.username)
    user_link.short_description = 'Utente'
    
    def event_link(self, obj):
        """Link all'evento"""
        url = reverse('admin:events_event_change', args=[obj.event.id])
        return format_html('<a href="{}">{}</a>', url, obj.event.title)
    event_link.short_description = 'Evento'
    
    def status_badge(self, obj):
        """Badge colorato per lo stato"""
        colors = {
            'pending': '#f59e0b',
            'confirmed': '#10b981',
            'cancelled': '#ef4444',
            'completed': '#6366f1'
        }
        
        return format_html(
            '<span style="background-color: {}; color: white; '
            'padding: 3px 10px; border-radius: 3px;">{}</span>',
            colors.get(obj.status, '#6b7280'),
            obj.get_status_display()
        )
    status_badge.short_description = 'Stato'
    
    def confirm_bookings(self, request, queryset):
        """Azione per confermare prenotazioni multiple"""
        confirmed = 0
        for booking in queryset.filter(status='pending'):
            booking.confirm()
            confirmed += 1
        
        self.message_user(
            request, 
            f'{confirmed} prenotazioni confermate con successo.'
        )
    confirm_bookings.short_description = 'Conferma prenotazioni selezionate'
    
    def cancel_bookings(self, request, queryset):
        """Azione per cancellare prenotazioni multiple"""
        cancelled = 0
        for booking in queryset.exclude(status='cancelled'):
            if booking.is_cancellable:
                booking.cancel()
                cancelled += 1
        
        self.message_user(
            request, 
            f'{cancelled} prenotazioni cancellate con successo.'
        )
    cancel_bookings.short_description = 'Cancella prenotazioni selezionate'
    
    def get_queryset(self, request):
        """Ottimizza le query"""
        return super().get_queryset(request).select_related(
            'user', 'event', 'event__category'
        ).prefetch_related('items__ticket')
    
    def has_delete_permission(self, request, obj=None):
        """Disabilita l'eliminazione diretta delle prenotazioni"""
        return False

@admin.register(BookingItem)
class BookingItemAdmin(admin.ModelAdmin):
    """Admin per gli elementi delle prenotazioni"""
    list_display = [
        'booking_link', 'ticket', 'quantity', 'price', 'subtotal'
    ]
    list_filter = ['ticket__ticket_type', 'booking__status']
    search_fields = [
        'booking__booking_code', 'ticket__name', 
        'booking__user__username'
    ]
    readonly_fields = ['booking', 'ticket', 'quantity', 'price', 'subtotal']
    
    def booking_link(self, obj):
        """Link alla prenotazione"""
        url = reverse('admin:bookings_booking_change', args=[obj.booking.id])
        return format_html(
            '<a href="{}">{}</a>', 
            url, 
            obj.booking.booking_code
        )
    booking_link.short_description = 'Prenotazione'
    
    def has_add_permission(self, request):
        """Disabilita l'aggiunta manuale di elementi"""
        return False
    
    def has_delete_permission(self, request, obj=None):
        """Disabilita l'eliminazione di elementi"""
        return False
    
    def get_queryset(self, request):
        """Ottimizza le query"""
        return super().get_queryset(request).select_related(
            'booking', 'booking__user', 'ticket', 'ticket__event'
        )