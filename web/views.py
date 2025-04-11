from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from web.forms import RegistrationForm, AuthForm, ToDoListForm, TagsForm, TodoListFilterForm
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.core.paginator import Paginator
from web.models import TodoList, ToDoTags

User = get_user_model()


def main_view(request):
    if not request.user.is_anonymous:
        todolists = TodoList.objects.filter(user=request.user).order_by('-priority')

        filter_form = TodoListFilterForm(request.GET)
        filter_form.is_valid()
        filters = filter_form.cleaned_data

        if filters.get('search'):
            todolists = todolists.filter(title__icontains=filters['search']) #icontains - поиск подстроки в title без учета регистра

        if filters.get('tag_name'):
            todolists = todolists.filter(tags=filters['tag_name'])

        if filters.get('priority_name'):
            todolists = todolists.filter(priority=filters['priority_name'])

        total_count = todolists.count()pus
        todolists = todolists.prefetch_related("tags")
        page_number = request.GET.get("page", 1)
        paginator = Paginator(todolists, per_page=15)

        return render(request, "web/main.html", {
            "todolists": paginator.get_page(page_number),
            "filter_form": filter_form,
            "total_count": total_count,
        })
    else:
        return render(request, "web/main.html")



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

@login_required()
def todo_list_edit_view(request, id=None):
    todolist = get_object_or_404(TodoList, user=request.user, id=id) if id is not None else None
    form = ToDoListForm(instance=todolist)
    if request.method == 'POST':
        form = ToDoListForm(data=request.POST, files=request.FILES, instance=todolist, initial={"user": request.user})
        if form.is_valid():
            form.save()
            return redirect("main")
    return render(request, "web/todo_list_form.html", {"form": form})

@login_required()
def todolist_delete_view(request, id):
    todolist = get_object_or_404(TodoList, user=request.user, id=id)
    todolist.delete()
    return redirect('main')

@login_required()
def tags_view(request, id=None):
    tags = ToDoTags.objects.all()
    form = TagsForm()
    if request.method == 'POST':
        form = TagsForm(data=request.POST, initial={"user": request.user})
        if form.is_valid():
            form.save()
            return redirect('tags')
    return render(request, "web/tags.html", {"tags": tags, "form": form})

@login_required()
def tags_delete_view(request, id):
    tag = get_object_or_404(ToDoTags, user=request.user, id=id)
    tag.delete()
    return redirect('tags')
