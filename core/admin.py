from django.contrib import admin
from .models import Lesson, Expression, Comment, ForumPost

class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'country', 'difficulty', 'created_at')
    search_fields = ('title', 'country')
    list_filter = ('category', 'difficulty', 'country')

class ExpressionAdmin(admin.ModelAdmin):
    list_display = ('text', 'lesson', 'meaning', 'created_at')
    search_fields = ('text', 'meaning', 'lesson__title')
    list_filter = ('lesson',)

admin.site.register(Lesson, LessonAdmin)
admin.site.register(Expression, ExpressionAdmin)
admin.site.register(Comment)
admin.site.register(ForumPost)
