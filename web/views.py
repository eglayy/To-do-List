from django.shortcuts import render, redirect
from datetime import datetime
from web.forms import RegistrationForm, AuthForm, ToDoListForm
from django.contrib.auth import get_user_model, authenticate, login, logout

from web.models import TodoList

User = get_user_model()


def main_view(request):
    todolists = TodoList.objects.all()
    return render(request, "web/main.html", {"todolists": todolists})


def registration_view(request):
    form = RegistrationForm()
    is_success = False
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            user = User(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
            )
            user.set_password(form.cleaned_data['password'])
            user.save()
            is_success = True
    return render(request, "web/registration.html", {
        "form": form, "is_success": is_success
    })


def auth_view(request):
    form = AuthForm()
    if request.method == 'POST':
        form = AuthForm(data=request.POST)
        if form.is_valid():
            user = authenticate(**form.cleaned_data)
            if user == None:
                form.add_error(None, "Пользователь не существует")
            else:
                login(request, user)
                return redirect("main")
    return render(request, "web/auth.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("main")


def todo_list_edit_view(request, id=None):
    todolist = TodoList.objects.get(id=id) if id is not None else None
    form = ToDoListForm(instance=todolist)
    if request.method == 'POST':
        form = ToDoListForm(data=request.POST, files=request.FILES, instance=todolist, initial={"user": request.user})
        if form.is_valid():
            form.save()
            return redirect("main")
    return render(request, "web/todo_list_form.html", {"form": form})
