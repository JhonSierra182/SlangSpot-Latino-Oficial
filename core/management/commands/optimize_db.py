from django.core.management.base import BaseCommand
from django.db import connection
from django.utils import timezone
from datetime import timedelta
from core.models import Lesson, Expression, ForumPost, Comment


class Command(BaseCommand):
    help = 'Optimiza la base de datos y limpia datos innecesarios'

    def add_arguments(self, parser):
        parser.add_argument(
            '--cleanup',
            action='store_true',
            help='Limpiar datos antiguos e inactivos',
        )
        parser.add_argument(
            '--vacuum',
            action='store_true',
            help='Ejecutar VACUUM en la base de datos (SQLite)',
        )
        parser.add_argument(
            '--analyze',
            action='store_true',
            help='Analizar estadísticas de la base de datos',
        )

    def handle(self, *args, **options):
        self.stdout.write('🔧 Iniciando optimización de base de datos...')
        
        if options['cleanup']:
            self.cleanup_data()
        
        if options['vacuum']:
            self.vacuum_database()
        
        if options['analyze']:
            self.analyze_database()
        
        if not any([options['cleanup'], options['vacuum'], options['analyze']]):
            # Ejecutar todas las optimizaciones por defecto
            self.cleanup_data()
            self.analyze_database()
        
        self.stdout.write(self.style.SUCCESS('✅ Optimización completada'))

    def cleanup_data(self):
        """Limpiar datos antiguos e inactivos"""
        self.stdout.write('🧹 Limpiando datos antiguos...')
        
        # Fecha límite: 1 año atrás
        cutoff_date = timezone.now() - timedelta(days=365)
        
        # Limpiar comentarios antiguos de posts eliminados
        deleted_comments = Comment.objects.filter(
            post__isnull=True
        ).count()
        Comment.objects.filter(post__isnull=True).delete()
        
        # Limpiar expresiones sin lección
        orphaned_expressions = Expression.objects.filter(
            lesson__isnull=True
        ).count()
        Expression.objects.filter(lesson__isnull=True).delete()
        
        # Limpiar posts muy antiguos e inactivos
        old_posts = ForumPost.objects.filter(
            created_at__lt=cutoff_date,
            is_active=False
        ).count()
        ForumPost.objects.filter(
            created_at__lt=cutoff_date,
            is_active=False
        ).delete()
        
        self.stdout.write(f'   - Eliminados {deleted_comments} comentarios huérfanos')
        self.stdout.write(f'   - Eliminadas {orphaned_expressions} expresiones sin lección')
        self.stdout.write(f'   - Eliminados {old_posts} posts antiguos inactivos')

    def vacuum_database(self):
        """Ejecutar VACUUM en la base de datos SQLite"""
        self.stdout.write('💾 Ejecutando VACUUM en la base de datos...')
        
        with connection.cursor() as cursor:
            cursor.execute('VACUUM')
        
        self.stdout.write('   - VACUUM completado')

    def analyze_database(self):
        """Analizar estadísticas de la base de datos"""
        self.stdout.write('📊 Analizando estadísticas de la base de datos...')
        
        # Contar registros por modelo
        lesson_count = Lesson.objects.count()
        expression_count = Expression.objects.count()
        post_count = ForumPost.objects.count()
        comment_count = Comment.objects.count()
        
        # Contar registros activos
        active_lessons = Lesson.objects.filter(is_active=True).count()
        active_expressions = Expression.objects.filter(is_active=True).count()
        active_posts = ForumPost.objects.filter(is_active=True).count()
        active_comments = Comment.objects.filter(is_active=True).count()
        
        # Tamaño de la base de datos
        with connection.cursor() as cursor:
            cursor.execute("SELECT page_count * page_size as size FROM pragma_page_count(), pragma_page_size()")
            db_size = cursor.fetchone()[0]
        
        self.stdout.write('   📈 Estadísticas:')
        self.stdout.write(f'      - Lecciones: {active_lessons}/{lesson_count} activas')
        self.stdout.write(f'      - Expresiones: {active_expressions}/{expression_count} activas')
        self.stdout.write(f'      - Posts: {active_posts}/{post_count} activos')
        self.stdout.write(f'      - Comentarios: {active_comments}/{comment_count} activos')
        self.stdout.write(f'      - Tamaño DB: {db_size / 1024 / 1024:.2f} MB') 