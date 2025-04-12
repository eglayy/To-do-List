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

def import_todolists_from_csv(file):
    print(file)