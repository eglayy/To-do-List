from web.models import TodoList, ToDoTags
import csv


def filter_todolists(todolists_qs, filters: dict):
    if filters.get('search'):
        todolists_qs = todolists_qs.filter(
            title__icontains=filters['search'])  # icontains - поиск подстроки в title без учета регистра

    if filters.get('tag_name'):
        todolists_qs = todolists_qs.filter(tags=filters['tag_name'])

    if filters.get('priority_name'):
        todolists_qs = todolists_qs.filter(priority=filters['priority_name'])
    return todolists_qs

def export_todolists_csv(todolists_qs, response):
    writer = csv.writer(response)
    writer.writerow(("title", "body", "priority", "deadline", "is_done", "tags"))

    for todolist in todolists_qs:
        writer.writerow((
            todolist.title, todolist.body, todolist.priority, todolist.deadline, todolist.is_done,
            " ".join([tag.title for tag in todolist.tags.all()])
        ))

    return response

def import_todolists_from_csv(file, user_id):
    strs_from_file = (row.decode() for row in file)
    reader = csv.DictReader(strs_from_file)

    todolists = []
    todolist_tags = []
    for row in reader:
        todolists.append(TodoList(
            title=row["title"],
            body=row["body"],
            priority=row["priority"],
            deadline=row["deadline"],
            is_done=row["is_done"],
            user_id=user_id
        ))
        todolist_tags.append(row['tags'].split(" ") if row['tags'] else [])

    tags_map = dict(ToDoTags.objects.all().values_list("title", "id"))
    saved_todolists = TodoList.objects.bulk_create(todolists)

    todo_tags = []
    for todolist, todolist_tags_item in zip(saved_todolists, todolist_tags):
        for tag in todolist_tags_item:
            tag_id = tags_map[tag]
            todo_tags.append(
                TodoList.tags.through(todolist_id=todolist.id, todotags_id=tag_id)
            )
    TodoList.tags.through.objects.bulk_create(todo_tags)