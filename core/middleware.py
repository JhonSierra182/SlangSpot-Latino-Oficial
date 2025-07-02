import gzip
import json
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse
import time


class CompressionMiddleware(MiddlewareMixin):
    """
    Middleware para comprimir respuestas HTTP usando gzip
    """
    
    def process_response(self, request, response):
        # Solo comprimir respuestas de texto
        content_types = [
            'text/html',
            'text/css',
            'text/javascript',
            'application/javascript',
            'application/json',
            'text/plain',
        ]
        
        if not any(ct in response.get('Content-Type', '') for ct in content_types):
            return response
        
        # Solo comprimir si el cliente lo soporta
        if 'gzip' not in request.META.get('HTTP_ACCEPT_ENCODING', ''):
            return response
        
        # Solo comprimir respuestas suficientemente grandes
        if len(response.content) < 500:
            return response
        
        # Comprimir la respuesta
        gzip_content = gzip.compress(response.content)
        response.content = gzip_content
        response['Content-Encoding'] = 'gzip'
        response['Content-Length'] = len(gzip_content)
        
        return response


class CacheHeadersMiddleware(MiddlewareMixin):
    """
    Middleware para agregar headers de cache apropiados
    """
    
    def process_response(self, request, response):
        # Cache para archivos estáticos
        if request.path.startswith('/static/'):
            response['Cache-Control'] = 'public, max-age=86400'  # 24 horas
        # Cache para imágenes de media
        elif request.path.startswith('/media/'):
            response['Cache-Control'] = 'public, max-age=3600'   # 1 hora
        # Cache para páginas de contenido
        elif response.status_code == 200 and not request.path.startswith('/admin/'):
            response['Cache-Control'] = 'public, max-age=300'    # 5 minutos
        
        return response


class PerformanceMiddleware(MiddlewareMixin):
    """
    Middleware para monitorear el rendimiento de las vistas
    """
    
    def process_request(self, request):
        request.start_time = time.time()
    
    def process_response(self, request, response):
        if hasattr(request, 'start_time'):
            duration = time.time() - request.start_time
            # Agregar header con tiempo de respuesta para debugging
            response['X-Response-Time'] = f'{duration:.3f}s'
            
            # Log de rendimiento para respuestas lentas
            if duration > 1.0:  # Más de 1 segundo
                import logging
                logger = logging.getLogger('django.performance')
                logger.warning(
                    f'Slow response: {request.path} took {duration:.3f}s'
                )
        
        return response 