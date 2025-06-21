from django.views.generic import TemplateView
from django.utils import timezone
from events.models import Event

class HomeView(TemplateView):
    template_name = 'home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Ottieni gli eventi futuri ordinati per data
        featured_events = Event.objects.filter(
            is_active=True,
            date__gte=timezone.now()
        ).select_related('category').order_by('date')[:6]
        
        context['featured_events'] = featured_events
        return context