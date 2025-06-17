from django.views.generic import DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from ..models import UserProfile

class ProfileView(LoginRequiredMixin, DetailView):
    model = UserProfile
    template_name = 'core/profile/profile.html'
    context_object_name = 'profile'

    def get_object(self):
        return self.request.user.userprofile

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    template_name = 'core/profile/profile_form.html'
    fields = ['bio', 'preferred_language', 'learning_goals']
    success_url = reverse_lazy('core:profile')

    def get_object(self):
        return self.request.user.userprofile

    def form_valid(self, form):
        messages.success(self.request, 'Perfil actualizado exitosamente.')
        return super().form_valid(form) 