from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Admin personalizzato per il modello utente"""
    
    list_display = [
        'username', 'email', 'full_name', 'phone_number', 
        'bookings_count', 'total_spent', 'date_joined', 'is_active'
    ]
    
    list_filter = ['is_active', 'is_staff', 'date_joined', 'last_login']
    
    search_fields = ['username', 'email', 'first_name', 'last_name', 'phone_number']
    
    ordering = ['-date_joined']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Informazioni Aggiuntive', {
            'fields': ('phone_number', 'date_of_birth', 'address', 'city', 'postal_code')
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informazioni Personali', {
            'fields': ('email', 'first_name', 'last_name', 'phone_number')
        }),
    )
    
    def full_name(self, obj):
        """Mostra il nome completo dell'utente"""
        return obj.get_full_name() or obj.username
    full_name.short_description = 'Nome Completo'
    
    def bookings_count(self, obj):
        """Conta il numero di prenotazioni dell'utente"""
        count = obj.bookings.count()
        confirmed = obj.bookings.filter(status='confirmed').count()
        
        return format_html(
            '<span>{} totali<br/><small>{} confermate</small></span>',
            count, confirmed
        )
    bookings_count.short_description = 'Prenotazioni'
    
    def total_spent(self, obj):
        """Calcola il totale speso dall'utente"""
        total = sum(
            booking.total_amount 
            for booking in obj.bookings.filter(status='confirmed')
        )
        
        return format_html(
            '<span style="color: #10b981; font-weight: bold;">€{}</span>',
            f"{total:.2f}"
        )
    total_spent.short_description = 'Totale Speso'
    
    def get_queryset(self, request):
        """Ottimizza le query"""
        return super().get_queryset(request).prefetch_related('bookings')
    
    actions = ['activate_users', 'deactivate_users', 'export_users']
    
    def activate_users(self, request, queryset):
        """Attiva gli utenti selezionati"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} utenti attivati con successo.')
    activate_users.short_description = 'Attiva utenti selezionati'
    
    def deactivate_users(self, request, queryset):
        """Disattiva gli utenti selezionati"""
        # Escludi superuser dalla disattivazione
        queryset = queryset.exclude(is_superuser=True)
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} utenti disattivati con successo.')
    deactivate_users.short_description = 'Disattiva utenti selezionati'
    
    def export_users(self, request, queryset):
        """Esporta gli utenti selezionati (placeholder)"""
        self.message_user(
            request, 
            'Funzionalità di esportazione non ancora implementata.'
        )
    export_users.short_description = 'Esporta utenti selezionati'

# Personalizzazione del sito admin
admin.site.site_header = 'TicketBooking Admin'
admin.site.site_title = 'TicketBooking Admin'
admin.site.index_title = 'Benvenuto nel pannello di amministrazione'