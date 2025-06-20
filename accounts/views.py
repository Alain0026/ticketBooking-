from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, UpdateView, DetailView
from .forms import SignUpForm, ProfileForm
from .models import CustomUser

class SignUpView(CreateView):
    """Vista per la registrazione di nuovi utenti"""
    model = CustomUser
    form_class = SignUpForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        """Se il form è valido, salva l'utente e fa il login automatico"""
        user = form.save()
        login(self.request, user)
        messages.success(self.request, 'Account creato con successo! Benvenuto in TicketBooking.')
        return redirect(self.success_url)
    
    def form_invalid(self, form):
        """Se il form non è valido, mostra gli errori"""
        messages.error(self.request, 'Si sono verificati degli errori. Controlla i campi sottostanti.')
        return super().form_invalid(form)

class ProfileView(LoginRequiredMixin, DetailView):
    """Vista per visualizzare il profilo utente"""
    model = CustomUser
    template_name = 'accounts/profile.html'
    context_object_name = 'profile_user'
    
    def get_object(self):
        return self.request.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Aggiungi statistiche utente
        user_bookings = self.request.user.bookings.all()
        context['total_bookings'] = user_bookings.count()
        context['confirmed_bookings'] = user_bookings.filter(status='confirmed').count()
        context['total_spent'] = sum(b.total_amount for b in user_bookings.filter(status='confirmed'))
        context['upcoming_events'] = user_bookings.filter(
            status='confirmed',
            event__date__gte=timezone.now()
        ).order_by('event__date')[:5]
        return context

class EditProfileView(LoginRequiredMixin, UpdateView):
    """Vista per modificare il profilo utente"""
    model = CustomUser
    form_class = ProfileForm
    template_name = 'accounts/edit_profile.html'
    success_url = reverse_lazy('profile')
    
    def get_object(self):
        return self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, 'Profilo aggiornato con successo!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Si sono verificati degli errori. Controlla i campi sottostanti.')
        return super().form_invalid(form)