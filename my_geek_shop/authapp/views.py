from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth
from django.urls import reverse

from authapp.forms import ShopUserLoginForm


def login(request):
    title = 'вход'
    text = 'Вход в систему'

    login_form = ShopUserLoginForm(data=request.POST)
    if request.method == 'POST' and login_form.is_valid():
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect(reverse('index'))

    context = {
        'title': title,
        'text': text,
        'login_form': login_form,
    }
    return render(request, 'authapp/login.html', context)


# TODO: создать шаблоны login.html и прочие


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


def register_account(request):
    return HttpResponseRedirect(reverse('index'))


def edit_account(request):
    return HttpResponseRedirect(reverse('index'))