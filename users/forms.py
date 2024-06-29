from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

from catalog.forms import StyleFormMixin
from users.models import User


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    """
    Форма регистрации пользователя.
    """

    class Meta:
        model = User
        fields = ("email", "password1", "password2")


class UserProfileForm(StyleFormMixin, UserChangeForm):
    """
    Форма профиля пользователя.
    """

    class Meta:
        model = User
        fields = ["new_email", "phone", "avatar", "country"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["password"].widget = forms.HiddenInput()
