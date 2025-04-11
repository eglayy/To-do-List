import random
from datetime import timedelta
from random import randint
from web.models import TodoList,  User, ToDoTags
from django.core.management import BaseCommand
from django.utils.timezone import now


class Command(BaseCommand):
    def handle(self, *args, **options):
        current_date = now()
        user = User.objects.first()
        tags = ToDoTags.objects.filter(user=user)

        todolists = []

        for day_index in range(30):
            current_date -= timedelta(days=1)

            for list_index in range(randint(5, 10)):
                todolists.append(TodoList(
                    title=f"generated {day_index}-{list_index}",
                    body="auto",
                    deadline=current_date + timedelta(hours=randint(0, 12)),
                    priority=random.choice((1, 2, 3)),
                    is_done=random.choice([True, False]),
                    user=user,
                ))
        saved_lists = TodoList.objects.bulk_create(todolists)

        todolist_tags = []
        for todolist in saved_lists:
            count_of_tags = randint(0, len(tags))
            for tag_index in range(count_of_tags):
                todolist_tags.append(
                    TodoList.tags.through(todolist_id=todolist.id, todotags_id=tags[tag_index].id)
                )
        TodoList.tags.through.objects.bulk_create(todolist_tags)
