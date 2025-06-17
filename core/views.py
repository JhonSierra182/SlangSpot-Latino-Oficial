from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.conf import settings
import json
import requests
from .models import UserProfile, Conversation, Message
from django.db.models import Q

def home(request):
    """Vista para la página principal"""
    return render(request, 'core/home.html')

@login_required
def chat(request):
    """Vista para la página de chat"""
    return render(request, 'core/chat.html')

# ... resto del código existente ... 