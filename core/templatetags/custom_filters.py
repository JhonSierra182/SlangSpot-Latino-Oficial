from django import template
import re

register = template.Library()

@register.filter
def youtube_embed_url(url):
    if not url:
        return ''
    
    # Patrones comunes de URLs de YouTube
    patterns = [
        r'(?:https?://)?(?:www\.)?youtube\.com/watch\?v=([^&]+)',
        r'(?:https?://)?(?:www\.)?youtube\.com/embed/([^&]+)',
        r'(?:https?://)?(?:www\.)?youtu\.be/([^?]+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            video_id = match.group(1)
            return f'https://www.youtube.com/embed/{video_id}'
    
    return url 