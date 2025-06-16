from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from .validators import validate_file_size, validate_image_extension, validate_audio_extension
import uuid
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.

class BaseModel(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    def soft_delete(self):
        self.is_active = False
        self.deleted_at = timezone.now()
        self.save()

class Expression(BaseModel):
    lesson = models.ForeignKey('Lesson', on_delete=models.CASCADE, related_name='expressions', null=True, blank=True)
    text = models.CharField(max_length=200, null=True, blank=True)
    meaning = models.TextField(null=True, blank=True)
    example = models.TextField(null=True, blank=True)
    audio = models.FileField(upload_to='expression_audio/', null=True, blank=True)

    def __str__(self):
        return f"{self.text} - {self.lesson.title if self.lesson else ''}"

    class Meta:
        ordering = ['created_at']

def lesson_cover_path(instance, filename):
    # Generar un nombre único para la imagen
    ext = filename.split('.')[-1]
    filename = f"{instance.id}_{instance.title}_{uuid.uuid4().hex[:8]}.{ext}"
    return f'lesson_covers/{filename}'

class Lesson(BaseModel):
    DIFFICULTY_CHOICES = [
        ('beginner', 'Principiante'),
        ('intermediate', 'Intermedio'),
        ('advanced', 'Avanzado'),
    ]
    
    CATEGORY_CHOICES = [
        ('slang', 'Slang'),
        ('proverb', 'Proverbio'),
    ]
    
    COUNTRY_CHOICES = [
        ('AR', 'Argentina'),
        ('BO', 'Bolivia'),
        ('CL', 'Chile'),
        ('CO', 'Colombia'),
        ('CR', 'Costa Rica'),
        ('CU', 'Cuba'),
        ('DO', 'República Dominicana'),
        ('EC', 'Ecuador'),
        ('SV', 'El Salvador'),
        ('GT', 'Guatemala'),
        ('HN', 'Honduras'),
        ('MX', 'México'),
        ('NI', 'Nicaragua'),
        ('PA', 'Panamá'),
        ('PY', 'Paraguay'),
        ('PE', 'Perú'),
        ('PR', 'Puerto Rico'),
        ('ES', 'España'),
        ('UY', 'Uruguay'),
        ('VE', 'Venezuela'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    country = models.CharField(max_length=50, choices=COUNTRY_CHOICES)
    video_url = models.URLField(blank=True, null=True)
    cultural_notes = models.TextField(blank=True, null=True)
    cover_image = models.ImageField(
        upload_to=lesson_cover_path,
        blank=True,
        null=True,
        validators=[validate_file_size, validate_image_extension]
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lessons', null=True, blank=True)
    
    def get_difficulty_display(self):
        return dict(self.DIFFICULTY_CHOICES).get(self.difficulty, self.difficulty)
    
    def get_category_display(self):
        return dict(self.CATEGORY_CHOICES).get(self.category, self.category)
    
    def get_country_display(self):
        return dict(self.COUNTRY_CHOICES).get(self.country, self.country)
    
    def get_cover_image_url(self):
        if self.cover_image and hasattr(self.cover_image, 'url'):
            return self.cover_image.url
        return '/static/core/images/default-cover.jpg'
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Lección'
        verbose_name_plural = 'Lecciones'
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['difficulty']),
            models.Index(fields=['category']),
            models.Index(fields=['country']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return self.title

class ForumPost(BaseModel):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, blank=True)
    views = models.PositiveIntegerField(default=0)
    is_pinned = models.BooleanField(default=False)
    is_closed = models.BooleanField(default=False)
    tags = models.ManyToManyField('Tag', blank=True)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    def can_edit(self, user):
        return user.is_superuser or self.author == user

    def can_delete(self, user):
        return user.is_superuser or self.author == user

    def can_moderate(self, user):
        return user.is_superuser or user.is_staff

class Comment(BaseModel):
    post = models.ForeignKey(ForumPost, on_delete=models.CASCADE, related_name='comments', null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    likes = models.ManyToManyField(User, related_name='liked_comments', blank=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        if not self.author or not self.post:
            return "Comentario sin autor o post"
        return f'Comentario de {self.author.username} en {self.post.title}'

    def get_replies(self):
        return self.replies.filter(is_active=True).order_by('created_at')

class UserProfile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    reputation = models.IntegerField(default=0)
    website = models.URLField(max_length=200, blank=True)
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f'Perfil de {self.user.username}'

class Tag(BaseModel):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Category(BaseModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
