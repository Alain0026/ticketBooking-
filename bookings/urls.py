from django.urls import path
from . import views

urlpatterns = [
    path('create/<slug:slug>/', views.create_booking, name='create_booking'),
    path('confirm/<str:booking_code>/', views.booking_confirm, name='booking_confirm'),
    path('success/<str:booking_code>/', views.booking_success, name='booking_success'),
    path('my-bookings/', views.MyBookingsView.as_view(), name='my_bookings'),
    path('detail/<str:booking_code>/', views.booking_detail, name='booking_detail'),
    path('cancel/<str:booking_code>/', views.cancel_booking, name='cancel_booking'),
    path('check-availability/<int:ticket_id>/', views.check_ticket_availability, name='check_ticket_availability'),
]