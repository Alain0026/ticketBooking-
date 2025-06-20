from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import EventViewSet, TicketViewSet

router = DefaultRouter()
router.register(r'events', EventViewSet, basename='api-event')
router.register(r'tickets', TicketViewSet, basename='api-ticket')

urlpatterns = [
    path('', include(router.urls)),
]