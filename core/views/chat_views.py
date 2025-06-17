from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.conf import settings
import json
import requests

@login_required
def chat(request):
    """Vista para la página de chat"""
    return render(request, 'core/chat.html')

@login_required
@require_http_methods(["GET"])
def get_chat_history(request):
    """Obtener el historial de chat del usuario"""
    # Implementar lógica para obtener historial
    return JsonResponse({'messages': []})

@login_required
@require_http_methods(["POST"])
def send_message(request):
    """Enviar un mensaje al chat"""
    try:
        data = json.loads(request.body)
        message = data.get('message', '')
        # Implementar lógica para guardar mensaje
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

@login_required
@require_http_methods(["POST"])
def get_ai_response(request):
    """Obtener respuesta de la IA"""
    try:
        data = json.loads(request.body)
        message = data.get('message', '')
        # Implementar lógica para obtener respuesta de IA
        return JsonResponse({'response': 'Respuesta de prueba'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}) 