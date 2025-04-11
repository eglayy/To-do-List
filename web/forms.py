from django import forms
from django.contrib.auth import get_user_model
from web.models import TodoList, ToDoTags

User = get_user_model()


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['password'] != cleaned_data['password2']:
            self.add_error('password', "Пароли не совпадают")
        return cleaned_data

    class Meta:
        model = User
        fields = ("email", "username", "password", "password2")


class AuthForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


class ToDoListForm(forms.ModelForm):
    deadline = forms.DateTimeField(widget=forms.DateTimeInput(attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%m"), label="Дедлайн")
    priority = forms.ChoiceField(choices=TodoList.PRIORITY_CHOICES, widget=forms.Select, initial=TodoList.MEDIUM, label="Приоритет")

    def save(self, commit=True):
        self.instance.user = self.initial['user']
        return super().save(commit)

    class Meta:
        model = TodoList
        exclude = ('user', )


class TagsForm(forms.ModelForm):
    def save(self, commit=True):
        self.instance.user = self.initial['user']
        return super().save(commit)
    class Meta:
        model = ToDoTags
        fields = ("title", )


class TodoListFilterForm(forms.Form):
    search = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Поиск"}), required=False)
    tag_name = forms.ModelChoiceField(
        queryset=ToDoTags.objects.all(),
        widget=forms.Select,
        required=False,
        empty_label="Выбор тега"
    )
    priority_name = forms.ChoiceField(
        choices=[('', 'Выбор приоритета')] + TodoList.PRIORITY_CHOICES,
        widget=forms.Select,
        required=False
    )