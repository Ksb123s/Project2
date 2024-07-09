from django import forms

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserForm(UserCreationForm):

    email = forms.EmailField(label="이메일", help_text="사용할 이메일을 입력해 주세요")

    class Meta:
        model = User
        fields = ["username", "email"]
        labels = {"username": "아이디"}
