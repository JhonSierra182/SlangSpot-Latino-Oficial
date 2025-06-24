#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'slangspot.settings')
django.setup()

from django.urls import reverse
from django.template.loader import render_to_string
from django.template import Context, Template
from core.models import Lesson, Expression

# Simular exactamente lo que hace la vista
lesson = Lesson.objects.get(id=1)
expressions = lesson.expressions.filter(is_active=True)

print(f"Lección: {lesson.title}")
print(f"Expresiones: {expressions.count()}")

# Crear el contexto
context = {
    'lesson': lesson,
    'expressions': expressions,
}

# Probar el template de debug
try:
    template_content = """
{% extends 'core/base.html' %}

{% block content %}
<h1>Debug: {{ lesson.title }}</h1>
<p>Expresiones encontradas: {{ expressions.count }}</p>

{% for expression in expressions %}
<div>
    <h3>Expresión ID: {{ expression.id }}</h3>
    <p>Texto: {{ expression.text }}</p>
    <p>URL: {% url 'core:edit_expression' pk=expression.id %}</p>
</div>
{% endfor %}
{% endblock %}
"""
    
    template = Template(template_content)
    rendered = template.render(Context(context))
    print("Template renderizado exitosamente")
    print(rendered[:500])  # Mostrar los primeros 500 caracteres
    
except Exception as e:
    print(f"Error al renderizar template: {e}")
    import traceback
    traceback.print_exc()

# Probar el template original
try:
    rendered = render_to_string('core/lesson_detail.html', context)
    print("Template original renderizado exitosamente")
except Exception as e:
    print(f"Error con template original: {e}")
    import traceback
    traceback.print_exc() 