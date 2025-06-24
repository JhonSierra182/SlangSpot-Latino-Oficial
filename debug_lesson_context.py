#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'slangspot.settings')
django.setup()

from django.urls import reverse
from core.models import Lesson, Expression

# Obtener la lección
lesson = Lesson.objects.get(id=1)
print(f"Lección: {lesson.title}")

# Obtener las expresiones
expressions = lesson.expressions.filter(is_active=True)
print(f"Expresiones encontradas: {expressions.count()}")

for expression in expressions:
    print(f"  - Expresión ID: {expression.id}, Texto: {expression.text}")
    
    # Probar la URL de edit_expression
    try:
        url = reverse('core:edit_expression', kwargs={'pk': expression.id})
        print(f"    URL edit_expression: {url}")
    except Exception as e:
        print(f"    Error con edit_expression: {e}")
    
    # Probar la URL de delete_expression
    try:
        url = reverse('core:delete_expression', kwargs={'pk': expression.id})
        print(f"    URL delete_expression: {url}")
    except Exception as e:
        print(f"    Error con delete_expression: {e}")

# Verificar todas las URLs disponibles
print("\nURLs disponibles:")
from django.urls import get_resolver
resolver = get_resolver()
for pattern in resolver.url_patterns:
    if hasattr(pattern, 'url_patterns'):
        for sub_pattern in pattern.url_patterns:
            if hasattr(sub_pattern, 'name') and sub_pattern.name:
                print(f"  - {sub_pattern.name}")
    elif hasattr(pattern, 'name') and pattern.name:
        print(f"  - {pattern.name}") 