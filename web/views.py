from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from web.forms import RegistrationForm, AuthForm, ToDoListForm, TagsForm, TodoListFilterForm, ImportForm
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.core.paginator import Paginator
from django.db.models import Count, Min, Max, F, Q
from web.models import TodoList, ToDoTags
from django.db.models.functions import TruncDate
from web.services import filter_todolists, export_todolists_csv, import_todolists_from_csv
from django.http import HttpResponse

User = get_user_model()


def main_view(request):
    if not request.user.is_anonymous:
        todolists = TodoList.objects.filter(user=request.user, is_done=False).order_by('-priority')

        filter_form = TodoListFilterForm(request.GET)
        filter_form.is_valid()
        todolists = filter_todolists(todolists, filter_form.cleaned_data)

        total_count = todolists.count()
        todolists = todolists.prefetch_related("tags")

        page_number = request.GET.get("page", 1)
        paginator = Paginator(todolists, per_page=15)

        if request.GET.get("export") == "csv":
            response = HttpResponse(
                content_type='text/csv',
                headers={"Content-Disposition": "attachment; filename=todolists.csv"}
            )
            return export_todolists_csv(todolists, response)

        return render(request, "web/main.html", {
            "todolists": paginator.get_page(page_number),
            "filter_form": filter_form,
            "total_count": total_count,
        })
    else:
        return render(request, "web/main.html")

@login_required
def import_view(request):
    if request.method == "POST":
        form = ImportForm(files=request.FILES)
        if form.is_valid():
            import_todolists_from_csv(form.cleaned_data["file"], request.user.id)
            return redirect("main")
    return render(request, "web/import.html", {"form": ImportForm()})

@login_required
def analytic_view(request):
    overall_stats = TodoList.objects.aggregate(
       tasks_count=Count("id"),
       max_deadline=Max("deadline"),
       min_deadline=Min("deadline")
    )

    days_stat = (
        TodoList.objects.all()
        .annotate(date=TruncDate("deadline"))
        .values("date")
        .annotate(
            count=Count("id"),
            is_done_count=Count("id", filter=Q(is_done=True))
        ).order_by("-date")
    )

    return render(request, "web/analytic.html", {
        "overall_stats": overall_stats,
        "days_stat": days_stat,
    })

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

@login_required
def todo_list_edit_view(request, id=None):
    todolist = get_object_or_404(TodoList, user=request.user, id=id) if id is not None else None
    form = ToDoListForm(instance=todolist)
    if request.method == 'POST':
        form = ToDoListForm(data=request.POST, files=request.FILES, instance=todolist, initial={"user": request.user})
        if form.is_valid():
            form.save()
            return redirect("main")
    return render(request, "web/todo_list_form.html", {"form": form})

@login_required
def todolist_delete_view(request, id):
    todolist = get_object_or_404(TodoList, user=request.user, id=id)
    todolist.delete()
    return redirect('main')

def complete_task_view(request, id):
    todolist = get_object_or_404(TodoList, user=request.user, id=id)
    todolist.is_done = True
    todolist.save()
    return redirect('main')

@login_required
def completed_tasks_view(request):
    todolists = TodoList.objects.filter(user=request.user, is_done=True).order_by('-priority')

    filter_form = TodoListFilterForm(request.GET)
    filter_form.is_valid()
    todolists = filter_todolists(todolists, filter_form.cleaned_data)

    total_count = todolists.count()
    todolists = todolists.prefetch_related("tags")

    page_number = request.GET.get("page", 1)
    paginator = Paginator(todolists, per_page=15)

    if request.GET.get("export") == "csv":
        response = HttpResponse(
            content_type='text/csv',
            headers={"Content-Disposition": "attachment; filename=CompletedTodolists.csv"}
        )
        return export_todolists_csv(todolists, response)

    return render(request, "web/completed_tasks.html", {
        "todolists": paginator.get_page(page_number),
        "filter_form": filter_form,
        "total_count": total_count,
    })


@login_required
def tags_view(request, id=None):
    tags = ToDoTags.objects.all()
    form = TagsForm()
    if request.method == 'POST':
        form = TagsForm(data=request.POST, initial={"user": request.user})
        if form.is_valid():
            form.save()
            return redirect('tags')
    return render(request, "web/tags.html", {"tags": tags, "form": form})

@login_required
def tags_delete_view(request, id):
    tag = get_object_or_404(ToDoTags, user=request.user, id=id)
    tag.delete()
    return redirect('tags')
