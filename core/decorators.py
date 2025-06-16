from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps
from .permissions import (
    can_edit_lesson, can_delete_lesson,
    can_edit_expression, can_delete_expression,
    can_edit_comment, can_delete_comment,
    can_edit_post, can_delete_post
)

def login_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Debes iniciar sesión para acceder a esta página.')
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def lesson_edit_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        lesson = view_func.lesson
        if not can_edit_lesson(request.user, lesson):
            messages.error(request, 'No tienes permiso para editar esta lección.')
            return redirect('lesson_detail', lesson_id=lesson.id)
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def lesson_delete_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        lesson = view_func.lesson
        if not can_delete_lesson(request.user, lesson):
            messages.error(request, 'No tienes permiso para eliminar esta lección.')
            return redirect('lesson_detail', lesson_id=lesson.id)
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def expression_edit_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        expression = view_func.expression
        if not can_edit_expression(request.user, expression):
            messages.error(request, 'No tienes permiso para editar esta expresión.')
            return redirect('lesson_detail', lesson_id=expression.lesson.id)
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def expression_delete_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        expression = view_func.expression
        if not can_delete_expression(request.user, expression):
            messages.error(request, 'No tienes permiso para eliminar esta expresión.')
            return redirect('lesson_detail', lesson_id=expression.lesson.id)
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def comment_edit_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        comment = view_func.comment
        if not can_edit_comment(request.user, comment):
            messages.error(request, 'No tienes permiso para editar este comentario.')
            return redirect('lesson_detail', lesson_id=comment.expression.lesson.id)
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def comment_delete_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        comment = view_func.comment
        if not can_delete_comment(request.user, comment):
            messages.error(request, 'No tienes permiso para eliminar este comentario.')
            return redirect('lesson_detail', lesson_id=comment.expression.lesson.id)
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def post_edit_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        post = view_func.post
        if not can_edit_post(request.user, post):
            messages.error(request, 'No tienes permiso para editar esta publicación.')
            return redirect('forum_post_detail', post_id=post.id)
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def post_delete_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        post = view_func.post
        if not can_delete_post(request.user, post):
            messages.error(request, 'No tienes permiso para eliminar esta publicación.')
            return redirect('forum_post_detail', post_id=post.id)
        return view_func(request, *args, **kwargs)
    return _wrapped_view 