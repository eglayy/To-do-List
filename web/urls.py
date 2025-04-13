from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from web.views import main_view, registration_view, auth_view, logout_view, todo_list_edit_view, tags_view, \
tags_delete_view, todolist_delete_view, complete_task_view, completed_tasks_view, analytic_view, import_view

urlpatterns = [
    path('', main_view, name="main"),
    path("registration/", registration_view, name="registration"),
    path("auth/", auth_view, name="auth"),
    path("logout/", logout_view, name="logout"),
    path("todo_list/add/", todo_list_edit_view, name="todo_lists_add"),
    path("todo_list/<int:id>/", todo_list_edit_view, name="todo_lists_edit"),
    path("todo_list/<int:id>/delete/", todolist_delete_view, name="todo_lists_delete"),
    path("tags/", tags_view, name="tags"),
    path("tags/<int:id>/", tags_delete_view, name="tags_delete"),
    path("tags/<int:id>/complete/", complete_task_view, name="complete_task"),
    path("completed_tasks/", completed_tasks_view, name="completed_tasks"),
    path("analytic/", analytic_view, name="tasks_analytic"),
    path("import/", import_view, name="import"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)