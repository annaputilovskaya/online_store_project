import secrets

from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, UpdateView

from config.settings import EMAIL_HOST_USER
from users.forms import UserRegisterForm, UserProfileForm
from users.models import User
from users.services import generate_password


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.new_email = user.email
        user.save(update_fields=['token', 'is_active'])
        host = self.request.get_host()
        url = f'http://{host}/users/email_confirm/{token}/'
        send_mail(
            subject='Подтверждение почты',
            message=f'Здравствуйте. Для подтверждения адреса электронной почты, пожалуйста, перейдите по ссылке {url}. '
                    f'Служба поддержки Naomitex.',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))


def reset_password(request):

    if request.method == 'POST':
        email = request.POST.get('email')
        user = get_object_or_404(User, email=email)
        password = generate_password()
        user.set_password(password)
        user.save(update_fields=['token', 'is_active'])
        send_mail(
            subject='Восстановление пароля',
            message=f'Здравствуйте! Ваш пароль для доступа изменен: {password}. Служба поддержки Naomitex.',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return redirect(reverse('users:login'))
    return render(request, 'users/reset_password.html')


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        user = self.get_object()
        if user.email != form.cleaned_data['new_email']:
            user.new_email = form.cleaned_data['new_email']
            token = secrets.token_hex(16)
            user.new_token = token
            user.is_active = False
            user.save()
            host = self.request.get_host()
            url = f'http://{host}/users/change_email/{token}/'
            send_mail(
                subject='Подтверждение почты',
                message=f'Здравствуйте. Для подтверждения адреса электронной почты, '
                        f'пожалуйста, перейдите по ссылке {url}. Служба поддержки Naomitex.',
                from_email=EMAIL_HOST_USER,
                recipient_list=[user.new_email],
            )
            return redirect(reverse('users:login'))
        user.save()
        return super().form_valid(form)


def change_email(request, token):
    user = get_object_or_404(User, new_token=token)
    user.email = user.new_email
    user.token = user.new_token
    user.new_token = ''
    user.is_active = True
    user.save()
    return redirect('users:profile')
