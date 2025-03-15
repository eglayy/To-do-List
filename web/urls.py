from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from web.views import main_view, registration_view, auth_view, logout_view, todo_list_edit_view

urlpatterns = [
    path('', main_view, name="main"),
    path("registration/", registration_view, name="registration"),
    path("auth/", auth_view, name="auth"),
    path("logout/", logout_view, name="logout"),
    path("todo_list/add/", todo_list_edit_view, name="todo_lists_add"),
    path("todo_list/<int:id>/", todo_list_edit_view, name="todo_lists_edit")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)