from django.test import TestCase
from django.contrib.auth.models import User
from core.forms import (
    CustomUserCreationForm, ForumPostForm, CommentForm, 
    LessonForm, ExpressionForm, PracticeForm, UserProfileForm
)
from core.models import Lesson, Expression, Practice, UserProfile


class CustomUserCreationFormTest(TestCase):
    """Tests para el formulario de creación de usuarios"""
    
    def test_valid_user_creation(self):
        """Test: Crear un usuario válido"""
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'testpass123',
            'password2': 'testpass123'
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_user_creation_with_mismatched_passwords(self):
        """Test: Contraseñas que no coinciden"""
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'testpass123',
            'password2': 'differentpass123'
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)
    
    def test_user_creation_without_required_fields(self):
        """Test: Campos requeridos faltantes"""
        form_data = {
            'username': 'testuser',
            'password1': 'testpass123',
            'password2': 'testpass123'
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        self.assertIn('first_name', form.errors)
        self.assertIn('last_name', form.errors)
    
    def test_user_creation_save(self):
        """Test: Guardar un usuario desde el formulario"""
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'testpass123',
            'password2': 'testpass123'
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.first_name, 'Test')
        self.assertEqual(user.last_name, 'User')


class ForumPostFormTest(TestCase):
    """Tests para el formulario de posts del foro"""
    
    def test_valid_forum_post(self):
        """Test: Crear un post válido"""
        form_data = {
            'title': 'Test Post Title',
            'content': 'This is the content of the test post.',
            'category': 'general'
        }
        form = ForumPostForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_forum_post_without_title(self):
        """Test: Post sin título"""
        form_data = {
            'content': 'This is the content of the test post.',
            'category': 'general'
        }
        form = ForumPostForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)
    
    def test_forum_post_without_content(self):
        """Test: Post sin contenido"""
        form_data = {
            'title': 'Test Post Title',
            'category': 'general'
        }
        form = ForumPostForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('content', form.errors)
    
    def test_forum_post_invalid_category(self):
        """Test: Categoría inválida"""
        form_data = {
            'title': 'Test Post Title',
            'content': 'This is the content of the test post.',
            'category': 'invalid_category'
        }
        form = ForumPostForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('category', form.errors)


class CommentFormTest(TestCase):
    """Tests para el formulario de comentarios"""
    
    def test_valid_comment(self):
        """Test: Crear un comentario válido"""
        form_data = {
            'content': 'This is a test comment.'
        }
        form = CommentForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_comment_without_content(self):
        """Test: Comentario sin contenido"""
        form_data = {}
        form = CommentForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('content', form.errors)
    
    def test_comment_empty_content(self):
        """Test: Comentario con contenido vacío"""
        form_data = {
            'content': ''
        }
        form = CommentForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('content', form.errors)


class LessonFormTest(TestCase):
    """Tests para el formulario de lecciones"""
    
    def test_valid_lesson(self):
        """Test: Crear una lección válida"""
        form_data = {
            'title': 'Test Lesson',
            'content': 'This is the content of the test lesson.',
            'level': 'beginner',
            'category': 'slang',
            'country': 'CO',
            'video_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            'cultural_notes': 'Some cultural notes about Colombia.'
        }
        form = LessonForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_lesson_without_required_fields(self):
        """Test: Lección sin campos requeridos"""
        form_data = {
            'title': 'Test Lesson',
            'content': 'Test content'
        }
        form = LessonForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('country', form.errors)
    
    def test_lesson_invalid_country(self):
        """Test: País inválido"""
        form_data = {
            'title': 'Test Lesson',
            'content': 'Test content',
            'country': 'INVALID'
        }
        form = LessonForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('country', form.errors)
    
    def test_lesson_invalid_level(self):
        """Test: Nivel inválido"""
        form_data = {
            'title': 'Test Lesson',
            'content': 'Test content',
            'country': 'CO',
            'level': 'invalid_level'
        }
        form = LessonForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('level', form.errors)
    
    def test_lesson_invalid_category(self):
        """Test: Categoría inválida"""
        form_data = {
            'title': 'Test Lesson',
            'content': 'Test content',
            'country': 'CO',
            'category': 'invalid_category'
        }
        form = LessonForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('category', form.errors)


class ExpressionFormTest(TestCase):
    """Tests para el formulario de expresiones"""
    
    def test_valid_expression(self):
        """Test: Crear una expresión válida"""
        form_data = {
            'text': '¡Qué chimba!',
            'meaning': '¡Qué genial!',
            'example': '¡Qué chimba este lugar!'
        }
        form = ExpressionForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_expression_without_text(self):
        """Test: Expresión sin texto"""
        form_data = {
            'meaning': '¡Qué genial!',
            'example': '¡Qué chimba este lugar!'
        }
        form = ExpressionForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('text', form.errors)
    
    def test_expression_with_only_text(self):
        """Test: Expresión solo con texto (inválida según validación del modelo)"""
        form_data = {
            'text': '¡Qué chimba!'
        }
        form = ExpressionForm(data=form_data)
        self.assertFalse(form.is_valid())  # Debería fallar porque no tiene meaning ni example
    
    def test_expression_with_text_and_meaning(self):
        """Test: Expresión con texto y significado (válida)"""
        form_data = {
            'text': '¡Qué chimba!',
            'meaning': '¡Qué genial!'
        }
        form = ExpressionForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_expression_with_text_and_example(self):
        """Test: Expresión con texto y ejemplo (válida)"""
        form_data = {
            'text': '¡Qué chimba!',
            'example': '¡Qué chimba este lugar!'
        }
        form = ExpressionForm(data=form_data)
        self.assertTrue(form.is_valid())


class PracticeFormTest(TestCase):
    """Tests para el formulario de prácticas"""
    
    def test_valid_practice(self):
        """Test: Crear una práctica válida"""
        form_data = {
            'title': 'Test Practice',
            'content': 'This is the content of the test practice.',
            'difficulty': 'medium'
        }
        form = PracticeForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_practice_without_required_fields(self):
        """Test: Práctica sin campos requeridos"""
        form_data = {
            'title': 'Test Practice'
        }
        form = PracticeForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('content', form.errors)
    
    def test_practice_invalid_difficulty(self):
        """Test: Dificultad inválida"""
        form_data = {
            'title': 'Test Practice',
            'content': 'Test content',
            'difficulty': 'invalid_difficulty'
        }
        form = PracticeForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('difficulty', form.errors)


class UserProfileFormTest(TestCase):
    """Tests para el formulario de perfil de usuario"""
    
    def test_valid_user_profile(self):
        """Test: Crear un perfil válido"""
        form_data = {
            'bio': 'This is my bio.',
            'preferred_language': 'es',
            'learning_goals': 'I want to learn Spanish.'
        }
        form = UserProfileForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_user_profile_with_empty_fields(self):
        """Test: Perfil con campos vacíos (inválido porque preferred_language es requerido)"""
        form_data = {}
        form = UserProfileForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('preferred_language', form.errors)
    
    def test_user_profile_with_partial_data(self):
        """Test: Perfil con datos parciales (válido si incluye preferred_language)"""
        form_data = {
            'bio': 'Just a bio.',
            'preferred_language': 'es'
        }
        form = UserProfileForm(data=form_data)
        self.assertTrue(form.is_valid()) 