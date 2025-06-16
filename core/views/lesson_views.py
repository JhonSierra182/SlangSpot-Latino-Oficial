from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from ..models import Lesson, Expression
from ..forms import LessonForm, ExpressionForm
from .mixins import OwnerRequiredMixin, SuccessMessageMixin, SoftDeleteMixin, SearchMixin

class LessonListView(LoginRequiredMixin, SearchMixin, ListView):
    model = Lesson
    template_name = 'core/lessons_index.html'
    context_object_name = 'lessons'
    search_fields = ['title', 'description']

class LessonDetailView(LoginRequiredMixin, DetailView):
    model = Lesson
    template_name = 'core/lesson_detail.html'
    context_object_name = 'lesson'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['expressions'] = self.object.expressions.filter(is_active=True)
        return context

class LessonCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Lesson
    form_class = LessonForm
    template_name = 'core/create_lesson.html'
    success_url = reverse_lazy('lessons_index')
    success_message = '¡Lección creada exitosamente!'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class LessonUpdateView(LoginRequiredMixin, OwnerRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Lesson
    form_class = LessonForm
    template_name = 'core/edit_lesson.html'
    success_message = 'Lección actualizada exitosamente.'
    
    def get_success_url(self):
        return reverse_lazy('lesson_detail', kwargs={'lesson_id': self.object.id})

class LessonDeleteView(LoginRequiredMixin, OwnerRequiredMixin, SoftDeleteMixin, DeleteView):
    model = Lesson
    template_name = 'core/delete_lesson.html'
    success_url = reverse_lazy('lessons_index')

class ExpressionCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Expression
    form_class = ExpressionForm
    template_name = 'core/create_expression.html'
    success_message = '¡Expresión creada exitosamente!'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lesson'] = get_object_or_404(Lesson, id=self.kwargs['lesson_id'])
        return context
    
    def form_valid(self, form):
        form.instance.lesson = get_object_or_404(Lesson, id=self.kwargs['lesson_id'])
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('lesson_detail', kwargs={'lesson_id': self.kwargs['lesson_id']})

class ExpressionUpdateView(LoginRequiredMixin, OwnerRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Expression
    form_class = ExpressionForm
    template_name = 'core/edit_expression.html'
    success_message = 'Expresión actualizada exitosamente.'
    
    def get_success_url(self):
        return reverse_lazy('lesson_detail', kwargs={'lesson_id': self.object.lesson.id})

class ExpressionDeleteView(LoginRequiredMixin, OwnerRequiredMixin, SoftDeleteMixin, DeleteView):
    model = Expression
    template_name = 'core/delete_expression.html'
    
    def get_success_url(self):
        return reverse_lazy('lesson_detail', kwargs={'lesson_id': self.object.lesson.id}) 