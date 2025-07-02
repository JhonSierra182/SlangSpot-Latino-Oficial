from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from core.models import Expression, Lesson, Comment, ForumPost, UserProfile


class ExpressionModelTest(TestCase):
    """Tests para el modelo Expression"""
    
    def setUp(self):
        """Configuración inicial para los tests"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.lesson = Lesson.objects.create(
            user=self.user,
            title='Test Lesson',
            content='Test content',
            country='CO'
        )
    
    def test_expression_creation(self):
        """Test: Crear una expresión válida"""
        expression = Expression.objects.create(
            lesson=self.lesson,
            text='¡Qué chimba!',
            meaning='¡Qué genial!',
            example='¡Qué chimba este lugar!'
        )
        self.assertEqual(expression.text, '¡Qué chimba!')
        self.assertEqual(expression.meaning, '¡Qué genial!')
        self.assertEqual(expression.lesson, self.lesson)
    
    def test_expression_text_required(self):
        """Test: El campo text es obligatorio"""
        expression = Expression(
            lesson=self.lesson,
            meaning='Significado sin texto',
            example='Ejemplo sin texto'
        )
        with self.assertRaises(ValidationError):
            expression.full_clean()
    
    def test_expression_validation_without_meaning_and_example(self):
        """Test: Validación cuando no hay significado ni ejemplo"""
        expression = Expression(
            lesson=self.lesson,
            text='Test expression'
        )
        with self.assertRaises(ValidationError):
            expression.full_clean()
    
    def test_expression_validation_with_meaning_only(self):
        """Test: Validación cuando solo hay significado"""
        expression = Expression(
            lesson=self.lesson,
            text='Test expression',
            meaning='Test meaning'
        )
        try:
            expression.full_clean()
        except ValidationError:
            self.fail("Expression should be valid with meaning only")
    
    def test_expression_validation_with_example_only(self):
        """Test: Validación cuando solo hay ejemplo"""
        expression = Expression(
            lesson=self.lesson,
            text='Test expression',
            example='Test example'
        )
        try:
            expression.full_clean()
        except ValidationError:
            self.fail("Expression should be valid with example only")
    
    def test_expression_str_representation(self):
        """Test: Representación en string de la expresión"""
        expression = Expression.objects.create(
            lesson=self.lesson,
            text='Test expression',
            meaning='Test meaning'
        )
        expected = f"Test expression - {self.lesson.title}"
        self.assertEqual(str(expression), expected)
    
    def test_expression_without_lesson(self):
        """Test: Expresión sin lección asociada"""
        expression = Expression.objects.create(
            text='Test expression',
            meaning='Test meaning'
        )
        self.assertIsNone(expression.lesson)
        self.assertEqual(str(expression), "Test expression - ")


class LessonModelTest(TestCase):
    """Tests para el modelo Lesson"""
    
    def setUp(self):
        """Configuración inicial para los tests"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_lesson_creation(self):
        """Test: Crear una lección válida"""
        lesson = Lesson.objects.create(
            user=self.user,
            title='Test Lesson',
            content='Test content for the lesson',
            country='CO',
            level='beginner',
            category='grammar'
        )
        self.assertEqual(lesson.title, 'Test Lesson')
        self.assertEqual(lesson.user, self.user)
        self.assertEqual(lesson.country, 'CO')
    
    def test_lesson_validation_empty_content(self):
        """Test: Validación cuando el contenido está vacío"""
        lesson = Lesson(
            user=self.user,
            title='Test Lesson',
            content='',
            country='CO'
        )
        with self.assertRaises(ValidationError):
            lesson.full_clean()
    
    def test_lesson_validation_default_content(self):
        """Test: Validación cuando el contenido es el valor por defecto"""
        lesson = Lesson(
            user=self.user,
            title='Test Lesson',
            content='Contenido pendiente',
            country='CO'
        )
        with self.assertRaises(ValidationError):
            lesson.full_clean()
    
    def test_lesson_str_representation(self):
        """Test: Representación en string de la lección"""
        lesson = Lesson.objects.create(
            user=self.user,
            title='Test Lesson',
            content='Test content',
            country='CO'
        )
        self.assertEqual(str(lesson), 'Test Lesson')
    
    def test_lesson_get_difficulty_display(self):
        """Test: Obtener el display del nivel de dificultad"""
        lesson = Lesson.objects.create(
            user=self.user,
            title='Test Lesson',
            content='Test content',
            country='CO',
            level='intermediate'
        )
        self.assertEqual(lesson.get_difficulty_display(), 'Intermedio')
    
    def test_lesson_get_category_display(self):
        """Test: Obtener el display de la categoría"""
        lesson = Lesson.objects.create(
            user=self.user,
            title='Test Lesson',
            content='Test content',
            country='CO',
            category='vocabulary'
        )
        self.assertEqual(lesson.get_category_display(), 'Vocabulario')
    
    def test_lesson_get_country_display(self):
        """Test: Obtener el display del país"""
        lesson = Lesson.objects.create(
            user=self.user,
            title='Test Lesson',
            content='Test content',
            country='MX'
        )
        self.assertEqual(lesson.get_country_display(), 'México')


class CommentModelTest(TestCase):
    """Tests para el modelo Comment"""
    
    def setUp(self):
        """Configuración inicial para los tests"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.post = ForumPost.objects.create(
            title='Test Post',
            content='Test content',
            author=self.user
        )
    
    def test_comment_creation(self):
        """Test: Crear un comentario válido"""
        comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            content='Test comment content'
        )
        self.assertEqual(comment.content, 'Test comment content')
        self.assertEqual(comment.post, self.post)
        self.assertEqual(comment.author, self.user)
    
    def test_comment_author_required(self):
        """Test: El campo author es obligatorio"""
        with self.assertRaises(Exception):
            Comment.objects.create(
                post=self.post,
                content='Test comment without author'
            )
    
    def test_comment_post_required(self):
        """Test: El campo post es obligatorio"""
        with self.assertRaises(Exception):
            Comment.objects.create(
                author=self.user,
                content='Test comment without post'
            )
    
    def test_comment_str_representation(self):
        """Test: Representación en string del comentario"""
        comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            content='Test comment'
        )
        expected = f'Comentario de {self.user.username} en {self.post.title}'
        self.assertEqual(str(comment), expected)
    
    def test_comment_replies(self):
        """Test: Sistema de respuestas a comentarios"""
        parent_comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            content='Parent comment'
        )
        reply = Comment.objects.create(
            post=self.post,
            author=self.user,
            content='Reply to parent',
            parent=parent_comment
        )
        replies = parent_comment.get_replies()
        self.assertIn(reply, replies)
        self.assertEqual(replies.count(), 1)


class UserProfileModelTest(TestCase):
    """Tests para el modelo UserProfile"""
    
    def setUp(self):
        """Configuración inicial para los tests"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_userprofile_creation(self):
        """Test: Crear un perfil de usuario válido"""
        profile = UserProfile.objects.create(
            user=self.user,
            bio='Test bio',
            preferred_language='es',
            learning_goals='Learn Spanish'
        )
        self.assertEqual(profile.user, self.user)
        self.assertEqual(profile.bio, 'Test bio')
        self.assertEqual(profile.preferred_language, 'es')
    
    def test_userprofile_str_representation(self):
        """Test: Representación en string del perfil"""
        profile = UserProfile.objects.create(
            user=self.user,
            bio='Test bio'
        )
        expected = f"{self.user.username}'s profile"
        self.assertEqual(str(profile), expected)
    
    def test_userprofile_default_values(self):
        """Test: Valores por defecto del perfil"""
        profile = UserProfile.objects.create(user=self.user)
        self.assertEqual(profile.preferred_language, 'es')
        self.assertEqual(profile.reputation, 0)
        self.assertEqual(profile.bio, '')
        self.assertEqual(profile.learning_goals, '') 