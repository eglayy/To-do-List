from django import forms
from django.contrib.auth import get_user_model

from web.models import TodoList, Priority

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
    deadline = forms.CharField(widget=forms.DateTimeInput(attrs={"type": "datetime-local"}))
    priority = forms.ChoiceField(choices=Priority.PRIORITY_CHOICES, widget=forms.Select, initial=Priority.MEDIUM)

    def save(self, commit=True):
        self.instance.user = self.initial['user']
        return super().save(commit)

    class Meta:
        model = TodoList
        fields = ("title", "body", "image", "tags")
