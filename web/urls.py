from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from web.views import main_view, registration_view, auth_view, logout_view, todo_list_edit_view, tags_view, \
tags_delete_view, todolist_delete_view, analytics_view, task_complete_view

urlpatterns = [
    path('', main_view, name="main"),
    path("registration/", registration_view, name="registration"),
    path("analytics/", analytics_view, name="analytics"),
    path("auth/", auth_view, name="auth"),
    path("logout/", logout_view, name="logout"),
    path("todo_list/add/", todo_list_edit_view, name="todo_lists_add"),
    path("todo_list/<int:id>/", todo_list_edit_view, name="todo_lists_edit"),
    path("todo_list/<int:id>/delete/", todolist_delete_view, name="todo_lists_delete"),
    path("tags/", tags_view, name="tags"),
    path("tags/<int:id>", tags_delete_view, name="tags_delete"),
    path("todo_list/<int:id>/complete", task_complete_view, name="task_complete"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)