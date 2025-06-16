from .auth_views import (
    home, registro, login_view, logout_view,
    notifications_view, mark_notification_read,
    mark_all_notifications_read
)

from .forum_views import (
    ForumPostListView, ForumPostDetailView,
    ForumPostCreateView, ForumPostUpdateView,
    ForumPostDeleteView, post_detail_view,
    like_post
)

from .lesson_views import (
    LessonListView, LessonDetailView,
    LessonCreateView, LessonUpdateView,
    LessonDeleteView, ExpressionCreateView,
    ExpressionUpdateView, ExpressionDeleteView
) 