from django.db import transaction
from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings

from authapp.forms import ShopUserLoginForm, ShopUserRegisterForm, ShopUserEditForm, ShopUserProfileEditForm
from authapp.models import ShopUser



def login(request):
    title = 'вход'
    text = 'login to the system'

    login_form = ShopUserLoginForm(data=request.POST or None)
    next_url = request.GET['next'] if 'next' in request.GET.keys() else ''
    if request.method == 'POST' and login_form.is_valid():
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            if 'next' in request.POST.keys():
                return HttpResponseRedirect(request.POST['next'])

            return HttpResponseRedirect(reverse('index'))

    context = {
        'title': title,
        'text': text,
        'login_form': login_form,
        'next': next_url,
    }
    return render(request, 'authapp/login.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


def register_account(request):
    title = 'регистрация'
    text = 'register'
    if request.method == 'POST':
        register_form = ShopUserRegisterForm(request.POST, request.FILES)

        if register_form.is_valid():
            user = register_form.save()

            if send_verify_mail(user):
                print('сообщение подтверждения отправлено')
                return HttpResponseRedirect(reverse('auth:login'))
            else:
                print('ошибка отправки сообщения')
                return HttpResponseRedirect(reverse('auth:login'))

    register_form = ShopUserRegisterForm()
    context = {
        'title': title,
        'text': text,
        'register_form': register_form,
    }
    return render(request, 'authapp/register.html', context)


@transaction.atomic
def edit_account(request):
    title = 'редактирование'
    text = 'edit account'

    if request.method == 'POST':
        edit_form = ShopUserEditForm(request.POST, request.FILES, instance=request.user)
        profile_form = ShopUserProfileEditForm(request.POST, instance=request.user.shopuserprofile)

        if edit_form.is_valid() and profile_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('auth:edit'))

    edit_form = ShopUserEditForm(instance=request.user)
    profile_form = ShopUserProfileEditForm()
    context = {
        'title': title,
        'text': text,
        'edit_form': edit_form,
        'profile_form': profile_form,
    }
    return render(request, 'authapp/edit.html', context)


def send_verify_mail(user: ShopUser):
    verify_link = reverse('auth:verify', args=[user.email, user.activation_key])
    title = f'Подтверждение учетной записи {user.username} '
    message = f'Для подтверждения учетной записи {user.username} ' \
              f'на портале {settings.DOMAIN_NAME} ' \
              f'перейдите по ссылке: {settings.DOMAIN_NAME}{verify_link}'
    return send_mail(
        title,
        message,
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False,
    )


def verify(request, email: str, activation_key: str):
    try:
        user = ShopUser.objects.get(email=email)
        if user.activation_key == activation_key and user.is_activation_key_not_expired():
            user.is_active = True
            user.save()
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return render(request, 'authapp/verification.html')
        else:
            print(f'Error activation user: {user}')
            return render(request, 'authapp/verification.html')
    except Exception as e:
        print(f'Error activation user: {e.args}')
        return HttpResponseRedirect(reverse('index'))

