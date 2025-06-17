from django.urls import path
from .views import (
    # Auth views
    home, registro, login_view, logout_view,
    notifications_view, mark_notification_read,
    mark_all_notifications_read,
    
    # Forum views
    ForumPostListView, ForumPostDetailView,
    ForumPostCreateView, ForumPostUpdateView,
    ForumPostDeleteView, post_detail_view,
    like_post,
    
    # Lesson views
    LessonListView, LessonDetailView,
    LessonCreateView, LessonUpdateView,
    LessonDeleteView, ExpressionCreateView,
    ExpressionUpdateView, ExpressionDeleteView,
    
    # Chat views
    chat, get_chat_history, send_message, get_ai_response,
    
    # Profile views
    ProfileView, ProfileUpdateView,
    
    # Practice views
    PracticeListView, PracticeCreateView,
    PracticeDetailView, PracticeUpdateView,
    PracticeDeleteView
)

app_name = 'core'

urlpatterns = [
    # Auth URLs
    path('', home, name='home'),
    path('registro/', registro, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('notifications/', notifications_view, name='notifications'),
    path('notifications/<int:notification_id>/read/', mark_notification_read, name='mark_notification_read'),
    path('notifications/mark-all-read/', mark_all_notifications_read, name='mark_all_notifications_read'),
    
    # Forum URLs
    path('forum/', ForumPostListView.as_view(), name='forum_index'),
    path('forum/post/<int:pk>/', ForumPostDetailView.as_view(), name='post_detail'),
    path('forum/post/create/', ForumPostCreateView.as_view(), name='create_post'),
    path('forum/post/<int:pk>/edit/', ForumPostUpdateView.as_view(), name='edit_post'),
    path('forum/post/<int:pk>/delete/', ForumPostDeleteView.as_view(), name='delete_post'),
    path('forum/post/<int:post_id>/like/', like_post, name='like_post'),
    
    # Lesson URLs
    path('lessons/', LessonListView.as_view(), name='lesson_list'),
    path('lessons/<int:pk>/', LessonDetailView.as_view(), name='lesson_detail'),
    path('lessons/create/', LessonCreateView.as_view(), name='create_lesson'),
    path('lessons/<int:pk>/edit/', LessonUpdateView.as_view(), name='edit_lesson'),
    path('lessons/<int:pk>/delete/', LessonDeleteView.as_view(), name='delete_lesson'),
    path('lessons/<int:lesson_id>/expressions/create/', ExpressionCreateView.as_view(), name='create_expression'),
    path('expressions/<int:pk>/edit/', ExpressionUpdateView.as_view(), name='edit_expression'),
    path('expressions/<int:pk>/delete/', ExpressionDeleteView.as_view(), name='delete_expression'),
    
    # Chat URLs
    path('chat/', chat, name='chat'),
    path('api/chat/history/', get_chat_history, name='chat_history'),
    path('api/chat/send/', send_message, name='send_message'),
    path('api/chat/response/', get_ai_response, name='get_ai_response'),
    
    # Profile URLs
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/edit/', ProfileUpdateView.as_view(), name='profile_edit'),
    
    # Practice URLs
    path('practice/', PracticeListView.as_view(), name='practice_list'),
    path('practice/create/', PracticeCreateView.as_view(), name='create_practice'),
    path('practice/<int:pk>/', PracticeDetailView.as_view(), name='practice_detail'),
    path('practice/<int:pk>/edit/', PracticeUpdateView.as_view(), name='practice_edit'),
    path('practice/<int:pk>/delete/', PracticeDeleteView.as_view(), name='practice_delete'),
] 