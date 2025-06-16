from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import ForumPost, Comment, Lesson, Expression

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email')  # Ahora pedimos username y email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "Nombre de usuario"
        self.fields['username'].help_text = None  # Oculta el texto de ayuda
        
        self.fields['email'].label = "Correo electrónico"
        self.fields['email'].required = True  # Hacemos el email obligatorio 
        
        self.fields['password1'].label = "Contraseña"
        self.fields['password2'].label = "Confirmar contraseña" 

class ForumPostForm(forms.ModelForm):
    class Meta:
        model = ForumPost
        fields = ['title', 'content', 'category', 'tags']
        labels = {
            'title': 'Título',
            'content': 'Contenido',
            'category': 'Categoría',
            'tags': 'Etiquetas (separadas por comas)'
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título de la publicación'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Contenido de la publicación', 'rows': 5}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'tags': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Etiquetas separadas por comas'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].label = "Título"
        self.fields['content'].label = "Contenido" 

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content': ''
        }
        widgets = {
            'content': forms.Textarea(attrs={'placeholder': 'Escribe tu comentario aquí...', 'rows': 3})
        }

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title', 'description', 'difficulty', 'category', 'country', 'video_url', 'cultural_notes', 'cover_image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título de la lección'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Descripción detallada de la lección'}),
            'difficulty': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'country': forms.Select(attrs={'class': 'form-control'}),
            'video_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'URL de YouTube (opcional)'}),
            'cultural_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Notas culturales (opcional)'}),
            'cover_image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }
        labels = {
            'title': 'Título',
            'description': 'Descripción',
            'difficulty': 'Nivel de Dificultad',
            'category': 'Categoría',
            'country': 'País',
            'video_url': 'URL del Video (YouTube)',
            'cultural_notes': 'Notas Culturales',
            'cover_image': 'Imagen de Portada',
        }

    def clean_video_url(self):
        url = self.cleaned_data.get('video_url')
        if url:
            if 'youtube.com' not in url and 'youtu.be' not in url:
                raise forms.ValidationError('Por favor, ingresa una URL válida de YouTube.')
            if 'watch?v=' in url:
                video_id = url.split('watch?v=')[1]
                return f'https://www.youtube.com/embed/{video_id}'
            elif 'youtu.be/' in url:
                video_id = url.split('youtu.be/')[1]
                return f'https://www.youtube.com/embed/{video_id}'
        return url

class ExpressionForm(forms.ModelForm):
    class Meta:
        model = Expression
        fields = ['text', 'meaning', 'example', 'audio']
        labels = {
            'text': 'Expresión',
            'meaning': 'Significado',
            'example': 'Ejemplo de uso',
            'audio': 'Audio (opcional)',
        }
        widgets = {
            'text': forms.TextInput(attrs={'placeholder': 'Escribe la expresión o frase...'}),
            'meaning': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Explica el significado...'}),
            'example': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Ejemplo de uso en contexto...'}),
            'audio': forms.FileInput(attrs={'accept': 'audio/*'}),
        } 