import os
from django.conf import settings
import tempfile
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.utils import timezone
from django.db.models import Q, Count
from .models import ForumPost, Comment, UserProfile

def generate_audio(text, filename):
    """
    Genera un archivo de audio usando ElevenLabs API
    """
    try:
        # Configurar la API key
        set_api_key(settings.ELEVENLABS_API_KEY)
        
        # Generar el audio
        audio = generate(
            text=text,
            voice="Josh",  # Voz en inglés
            model="eleven_monolingual_v1"
        )
        
        # Crear el directorio si no existe
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        # Guardar el audio
        save(audio, filename)
        
        return True
    except Exception as e:
        print(f"Error generando audio: {str(e)}")
        return False 

def create_notification(user, notification_type, message, related_post=None, related_comment=None, related_user=None):
    """
    Crea una notificación y la envía en tiempo real al usuario
    """
    notification = Notification.objects.create(
        user=user,
        notification_type=notification_type,
        message=message,
        related_post=related_post,
        related_comment=related_comment,
        related_user=related_user
    )

    # Enviar notificación en tiempo real
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"user_{user.id}_notifications",
        {
            "type": "send_notification",
            "message": message,
            "notification_id": notification.id,
            "notification_type": notification_type,
            "data": {
                "post_id": related_post.id if related_post else None,
                "comment_id": related_comment.id if related_comment else None,
                "user_id": related_user.id if related_user else None,
            }
        }
    )

    return notification

def notify_post_like(post, user):
    """
    Notifica al autor de un post cuando recibe un like
    """
    if post.author != user:  # No notificar si el usuario se da like a sí mismo
        message = f"{user.username} dio me gusta a tu publicación '{post.title}'"
        create_notification(
            user=post.author,
            notification_type='post_like',
            message=message,
            related_post=post,
            related_user=user
        )

def notify_comment_like(comment, user):
    """
    Notifica al autor de un comentario cuando recibe un like
    """
    if comment.user != user:  # No notificar si el usuario se da like a sí mismo
        message = f"{user.username} dio me gusta a tu comentario"
        create_notification(
            user=comment.user,
            notification_type='comment_like',
            message=message,
            related_comment=comment,
            related_user=user
        )

def notify_new_comment(post, comment, user):
    """
    Notifica al autor de un post cuando recibe un nuevo comentario
    """
    if post.author != user:  # No notificar si el autor comenta su propio post
        message = f"{user.username} comentó en tu publicación '{post.title}'"
        create_notification(
            user=post.author,
            notification_type='new_comment',
            message=message,
            related_post=post,
            related_comment=comment,
            related_user=user
        )

def notify_reply(comment, reply, user):
    """
    Notifica al autor de un comentario cuando recibe una respuesta
    """
    if comment.user != user:  # No notificar si el usuario responde a su propio comentario
        message = f"{user.username} respondió a tu comentario"
        create_notification(
            user=comment.user,
            notification_type='reply',
            message=message,
            related_comment=reply,
            related_user=user
        )

def notify_mention(user, mentioned_user, post=None, comment=None):
    """
    Notifica a un usuario cuando es mencionado
    """
    if user != mentioned_user:  # No notificar si el usuario se menciona a sí mismo
        context = "en un comentario" if comment else "en una publicación"
        message = f"{user.username} te mencionó {context}"
        create_notification(
            user=mentioned_user,
            notification_type='mention',
            message=message,
            related_post=post,
            related_comment=comment,
            related_user=user
        )

def notify_moderation(user, action, post=None, comment=None):
    """
    Notifica a un usuario sobre acciones de moderación
    """
    message = f"Tu {action} ha sido moderado"
    create_notification(
        user=user,
        notification_type='moderation',
        message=message,
        related_post=post,
        related_comment=comment
    )

def get_recent_activity(user, days=7):
    """Obtiene la actividad reciente de un usuario"""
    start_date = timezone.now() - timezone.timedelta(days=days)
    
    posts = ForumPost.objects.filter(
        author=user,
        created_at__gte=start_date
    ).order_by('-created_at')
    
    comments = Comment.objects.filter(
        author=user,
        created_at__gte=start_date
    ).order_by('-created_at')
    
    return {
        'posts': posts,
        'comments': comments
    }

def get_user_stats(user):
    """Obtiene estadísticas del usuario"""
    return {
        'posts_count': ForumPost.objects.filter(author=user).count(),
        'comments_count': Comment.objects.filter(author=user).count(),
        'likes_received': ForumPost.objects.filter(author=user).aggregate(
            total_likes=Count('likes')
        )['total_likes'] or 0
    }

def search_posts(query):
    """Busca posts por título o contenido"""
    return ForumPost.objects.filter(
        Q(title__icontains=query) | Q(content__icontains=query)
    ).order_by('-created_at')

def get_popular_posts(days=30):
    """Obtiene los posts más populares"""
    start_date = timezone.now() - timezone.timedelta(days=days)
    return ForumPost.objects.filter(
        created_at__gte=start_date
    ).annotate(
        popularity=Count('likes') + Count('comments')
    ).order_by('-popularity')[:10]

def get_user_reputation(user):
    """Calcula la reputación del usuario"""
    profile = UserProfile.objects.get_or_create(user=user)[0]
    return profile.reputation 