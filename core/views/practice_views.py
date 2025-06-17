from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from ..models import Practice

class PracticeListView(LoginRequiredMixin, ListView):
    model = Practice
    template_name = 'core/practice/practice_list.html'
    context_object_name = 'practices'
    ordering = ['-created_at']

    def get_queryset(self):
        return Practice.objects.filter(user=self.request.user)

class PracticeCreateView(LoginRequiredMixin, CreateView):
    model = Practice
    template_name = 'core/practice/practice_form.html'
    fields = ['title', 'content', 'difficulty']
    success_url = reverse_lazy('core:practice_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Práctica creada exitosamente.')
        return super().form_valid(form)

class PracticeDetailView(LoginRequiredMixin, DetailView):
    model = Practice
    template_name = 'core/practice/practice_detail.html'
    context_object_name = 'practice'

    def get_queryset(self):
        return Practice.objects.filter(user=self.request.user)

class PracticeUpdateView(LoginRequiredMixin, UpdateView):
    model = Practice
    template_name = 'core/practice/practice_form.html'
    fields = ['title', 'content', 'difficulty']
    success_url = reverse_lazy('core:practice_list')

    def get_queryset(self):
        return Practice.objects.filter(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Práctica actualizada exitosamente.')
        return super().form_valid(form)

class PracticeDeleteView(LoginRequiredMixin, DeleteView):
    model = Practice
    template_name = 'core/practice/practice_confirm_delete.html'
    success_url = reverse_lazy('core:practice_list')
    context_object_name = 'practice'

    def get_queryset(self):
        return Practice.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Práctica eliminada exitosamente.')
        return super().delete(request, *args, **kwargs) 