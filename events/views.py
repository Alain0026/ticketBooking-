from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Q, Min
from django.utils import timezone
from .models import Event, EventCategory, Ticket

class EventListView(ListView):
    """Vista per la lista degli eventi"""
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'
    paginate_by = 9
    
    def get_queryset(self):
        queryset = Event.objects.filter(
            is_active=True,
            date__gte=timezone.now()
        ).select_related('category').prefetch_related('tickets')
        
        # Filtro per categoria
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category__slug=category)
        
        # Ricerca
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | 
                Q(description__icontains=search) |
                Q(venue__icontains=search) |
                Q(city__icontains=search)
            )
        
        # Ordinamento
        sort = self.request.GET.get('sort', 'date')
        if sort == 'price':
            queryset = queryset.annotate(min_price=Min('tickets__price')).order_by('min_price')
        else:
            queryset = queryset.order_by(sort)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = EventCategory.objects.all()
        context['current_category'] = self.request.GET.get('category', '')
        context['search_query'] = self.request.GET.get('search', '')
        context['current_sort'] = self.request.GET.get('sort', 'date')
        return context

class EventDetailView(DetailView):
    """Vista per il dettaglio di un evento"""
    model = Event
    template_name = 'events/event_detail.html'
    context_object_name = 'event'
    
    def get_queryset(self):
        return Event.objects.filter(is_active=True).select_related('category').prefetch_related('tickets')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tickets'] = self.object.tickets.filter(is_active=True)
        context['related_events'] = Event.objects.filter(
            category=self.object.category,
            is_active=True,
            date__gte=timezone.now()
        ).exclude(id=self.object.id)[:3]
        return context