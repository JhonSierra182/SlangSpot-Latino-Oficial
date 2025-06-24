from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from ..models import Lesson, Expression
from ..forms import LessonForm, ExpressionForm
from .mixins import OwnerRequiredMixin, SuccessMessageMixin, SoftDeleteMixin, SearchMixin

class LessonListView(LoginRequiredMixin, ListView):
    model = Lesson
    template_name = 'core/lessons_index.html'
    context_object_name = 'lessons'
    login_url = '/core/login/'
    
    def get_queryset(self):
        queryset = Lesson.objects.filter(is_active=True)
        
        # Búsqueda
        search_query = self.request.GET.get('q')
        if search_query:
            from django.db.models import Q
            queryset = queryset.filter(
                Q(title__icontains=search_query) | 
                Q(content__icontains=search_query)
            )
        
        # Filtros
        country_filter = self.request.GET.get('country')
        difficulty_filter = self.request.GET.get('difficulty')
        category_filter = self.request.GET.get('category')
        sort_by = self.request.GET.get('sort', '-created_at')
        
        if country_filter:
            queryset = queryset.filter(country=country_filter)
        if difficulty_filter:
            queryset = queryset.filter(level=difficulty_filter)
        if category_filter:
            queryset = queryset.filter(category=category_filter)
        
        return queryset.order_by(sort_by)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Agregar datos para filtros
        context['countries'] = Lesson.COUNTRY_CHOICES
        context['difficulties'] = Lesson.LEVEL_CHOICES
        context['categories'] = Lesson.CATEGORY_CHOICES
        
        # Valores actuales de filtros
        context['country_filter'] = self.request.GET.get('country')
        context['difficulty_filter'] = self.request.GET.get('difficulty')
        context['category_filter'] = self.request.GET.get('category')
        context['sort_by'] = self.request.GET.get('sort', '-created_at')
        context['search_query'] = self.request.GET.get('q', '')
        
        return context

# Vista temporal simple para debug - devuelve texto plano
class LessonDetailView(DetailView):
    model = Lesson
    template_name = 'core/lesson_detail.html'
    context_object_name = 'lesson'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        expressions = self.object.expressions.filter(is_active=True)
        context['expressions'] = expressions
        return context

class LessonCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Lesson
    form_class = LessonForm
    template_name = 'core/create_lesson.html'
    success_url = reverse_lazy('core:lesson_list')
    success_message = '¡Lección creada exitosamente!'
    login_url = '/core/login/'
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class LessonUpdateView(LoginRequiredMixin, OwnerRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Lesson
    form_class = LessonForm
    template_name = 'core/edit_lesson.html'
    success_message = 'Lección actualizada exitosamente.'
    login_url = '/core/login/'
    
    def get_success_url(self):
        return reverse_lazy('core:lesson_detail', kwargs={'pk': self.object.id})

class LessonDeleteView(LoginRequiredMixin, OwnerRequiredMixin, SoftDeleteMixin, DeleteView):
    model = Lesson
    template_name = 'core/delete_lesson.html'
    success_url = reverse_lazy('core:lesson_list')
    login_url = '/core/login/'

class ExpressionCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Expression
    form_class = ExpressionForm
    template_name = 'core/create_expression.html'
    success_message = '¡Expresión creada exitosamente!'
    login_url = '/core/login/'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lesson'] = get_object_or_404(Lesson, id=self.kwargs['lesson_id'])
        return context
    
    def form_valid(self, form):
        form.instance.lesson = get_object_or_404(Lesson, id=self.kwargs['lesson_id'])
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('core:lesson_detail', kwargs={'pk': self.kwargs['lesson_id']})

class ExpressionUpdateView(LoginRequiredMixin, OwnerRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Expression
    form_class = ExpressionForm
    template_name = 'core/edit_expression.html'
    success_message = 'Expresión actualizada exitosamente.'
    login_url = '/core/login/'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lesson'] = self.object.lesson
        return context
    
    def get_success_url(self):
        return reverse_lazy('core:lesson_detail', kwargs={'pk': self.object.lesson.id})

class ExpressionDeleteView(LoginRequiredMixin, OwnerRequiredMixin, SoftDeleteMixin, DeleteView):
    model = Expression
    template_name = 'core/delete_expression.html'
    login_url = '/core/login/'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lesson'] = self.object.lesson
        return context
    
    def get_success_url(self):
        return reverse_lazy('core:lesson_detail', kwargs={'pk': self.object.lesson.id}) 