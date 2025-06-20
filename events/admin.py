from django.contrib import admin
from django.utils.html import format_html
from .models import EventCategory, Event, Ticket

@admin.register(EventCategory)
class EventCategoryAdmin(admin.ModelAdmin):
    """Admin per le categorie di eventi"""
    list_display = ['name', 'slug', 'event_count']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']
    
    def event_count(self, obj):
        """Mostra il numero di eventi per categoria"""
        return obj.events.count()
    event_count.short_description = 'Numero Eventi'

class TicketInline(admin.TabularInline):
    """Inline per gestire i biglietti direttamente dall'evento"""
    model = Ticket
    extra = 1
    fields = ['name', 'ticket_type', 'price', 'quantity', 'sold_quantity', 'is_active']
    readonly_fields = ['sold_quantity']

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """Admin per gli eventi"""
    list_display = [
        'title', 'category', 'date', 'venue', 'city', 
        'status_badge', 'tickets_info', 'is_active'
    ]
    list_filter = ['category', 'is_active', 'date', 'city']
    search_fields = ['title', 'description', 'venue', 'city']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'date'
    inlines = [TicketInline]
    
    fieldsets = (
        ('Informazioni Principali', {
            'fields': ('title', 'slug', 'category', 'description', 'image')
        }),
        ('Dettagli Evento', {
            'fields': ('date', 'venue', 'address', 'city', 'max_capacity')
        }),
        ('Stato', {
            'fields': ('is_active',)
        }),
    )
    
    def status_badge(self, obj):
        """Mostra lo stato dell'evento con badge colorato"""
        if obj.is_past:
            return format_html(
                '<span style="background-color: #6b7280; color: white; '
                'padding: 3px 10px; border-radius: 3px;">Passato</span>'
            )
        elif obj.is_sold_out:
            return format_html(
                '<span style="background-color: #ef4444; color: white; '
                'padding: 3px 10px; border-radius: 3px;">Sold Out</span>'
            )
        else:
            return format_html(
                '<span style="background-color: #10b981; color: white; '
                'padding: 3px 10px; border-radius: 3px;">Disponibile</span>'
            )
    status_badge.short_description = 'Stato'
    
    def tickets_info(self, obj):
        """Mostra informazioni sui biglietti"""
        total = sum(t.quantity for t in obj.tickets.all())
        sold = sum(t.sold_quantity for t in obj.tickets.all())
        available = total - sold
        
        return format_html(
            '<span>{} / {} ({}%)</span>',
            sold, total, 
            int((sold / total * 100) if total > 0 else 0)
        )
    tickets_info.short_description = 'Biglietti (Venduti/Totali)'
    
    def get_queryset(self, request):
        """Ottimizza le query"""
        return super().get_queryset(request).select_related('category').prefetch_related('tickets')

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    """Admin per i biglietti"""
    list_display = [
        'name', 'event', 'ticket_type', 'price', 
        'availability_info', 'is_active'
    ]
    list_filter = ['ticket_type', 'is_active', 'event__category']
    search_fields = ['name', 'event__title']
    list_editable = ['price', 'is_active']
    
    fieldsets = (
        ('Informazioni Biglietto', {
            'fields': ('event', 'name', 'ticket_type', 'description')
        }),
        ('Prezzo e Disponibilità', {
            'fields': ('price', 'quantity', 'sold_quantity', 'max_per_order')
        }),
        ('Stato', {
            'fields': ('is_active',)
        }),
    )
    
    readonly_fields = ['sold_quantity']
    
    def availability_info(self, obj):
        """Mostra la disponibilità con barra di progresso"""
        available = obj.available_quantity
        total = obj.quantity
        percentage = (obj.sold_quantity / total * 100) if total > 0 else 0
        
        color = '#10b981' if percentage < 70 else '#f59e0b' if percentage < 90 else '#ef4444'
        
        return format_html(
            '<div style="width: 150px; background-color: #e5e7eb; '
            'border-radius: 3px; overflow: hidden;">'
            '<div style="width: {}%; background-color: {}; height: 20px; '
            'text-align: center; color: white; line-height: 20px;">'
            '{} / {}</div></div>',
            percentage, color, available, total
        )
    availability_info.short_description = 'Disponibilità'
    
    def get_queryset(self, request):
        """Ottimizza le query"""
        return super().get_queryset(request).select_related('event', 'event__category')