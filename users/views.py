from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages

from .forms import UserRegisterForm
from .models import User

class UserRegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')
    
    def form_valid(self, form):
        user = form.save()
        try:
            send_mail(
                subject='Добро пожаловать!',
                message=f'Приветствуем, {user.email}! Спасибо за регистрацию!',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
            messages.success(self.request, 'Регистрация успешна! Письмо отправлено.')
        except:
            messages.success(self.request, 'Регистрация успешна!')
        return super().form_valid(form)

class UserLoginView(LoginView):
    template_name = 'users/login.html'

class UserLogoutView(LogoutView):
    next_page = reverse_lazy('catalog:home')
