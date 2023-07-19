import re
import string
import datetime
import random

from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.signals import user_logged_out, user_logged_in
from django.contrib.auth import update_session_auth_hash
from .models import OnetimePassword


def logout(sender, user, request, **kwargs):
    ip = request.META.get('REMOTE_ADDR')
    messages.success(request, 'Du wurdest ausgeloggt.')


def loginsuccessful(sender, user, request, **kwargs):
    ip = request.META.get('REMOTE_ADDR')
    messages.success(request, 'Hallo ' + str(request.user.first_name) + ', du wurdest erfolgreich eingeloggt.')


user_logged_out.connect(logout)
user_logged_in.connect(loginsuccessful)


# Create your views here.
def home(request):
    if request.user.is_authenticated:
        dates = {}
        return render(request, 'sites/home.html', dates)

    else:
        return redirect('login')
    

def history(request):
    if request.user.is_authenticated:
        dates = {}
        return render(request, 'sites/home.html', dates)

    else:
        return redirect('login')
        

def new_password(request):
    if request.user.is_authenticated:
        dates = {}

        if request.method == 'POST':
            user = User.objects.get(username=request.user.username)

            name = request.POST.get('name')
            share_username = request.POST.get('username')
            password = request.POST.get('password')
            creator = user
            one_time_token = token_generator(size=get_random_size())
            token_expiry_date = datetime.datetime.strptime(request.POST.get('token_expiry_date'), "%Y-%m-%d").date()

            new_password_obj = OnetimePassword(
                name=name, username=share_username, password=password,
                creator=creator, one_time_token=one_time_token,
                token_expiry_date=token_expiry_date
            )
            new_password_obj.save()

            return redirect('home')

        return render(request, 'sites/new_password.html', dates)

    else:
        return redirect('login')
        

def new_message(request):
    if request.user.is_authenticated:
        dates = {}
        return render(request, 'sites/new_message.html', dates)

    else:
        return redirect('login')
    

def share_password_by_token(request, token):
    status = 'link_not_aviable'
    try:
        onetime_password = OnetimePassword.objects.get(one_time_token=token)
    except:
        dates = {'status': status}
        return render(request, 'sites/share_password_by_token.html', dates)
    
    token_expiry_date = onetime_password.token_expiry_date
    open_status = onetime_password.opend
    now = datetime.date.today()

    if now <= token_expiry_date and open_status == False:
        status = 'link_aviable'
        if request.method == 'POST':
            opener = request.POST.get('name')
            status = 'link_aviable_and_open'

            onetime_password.opend = True
            onetime_password.name_of_opener = opener
            onetime_password.save()


            dates = {'status': status,
                     'name': onetime_password.name,
                     'share_username': onetime_password.username,
                     'password': onetime_password.password
                     }
            return render(request, 'sites/share_password_by_token.html', dates)
        else:
            dates = {'status': status,
                     'name': onetime_password.name,
                     }
            return render(request, 'sites/share_password_by_token.html', dates)
    else:
        status = 'link_not_aviable_anymore'
        dates = {'status': status}
        return render(request, 'sites/share_password_by_token.html', dates)


def password_change(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PasswordChangeForm(user=request.user, data=request.POST)
            my_message = re.search('<ul class="errorlist"><li>(.+?)</li>', str(form))
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)
                messages.success(request, 'Du hast dein Passwort erfolgreich geändert')
                return redirect('home')
            else:
                messages.error(request,
                               str(my_message.group().replace('<ul class="errorlist"><li>', '').replace('</li>', '')))
                return render(request, 'sites/change_password.html')
        else:
            return render(request, 'sites/change_password.html')

    else:
        return redirect('login')


def settings(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            users = User.objects.get(first_name=request.user.first_name)
            # Nachnamen aendern und Log eintrag dazu erstellen
            try:
                if request.POST.get('firstname') != '':
                    users.first_name = request.POST.get('firstname')
                    users.save()

                if request.POST.get('lastname') != '':
                    users.last_name = request.POST.get('lastname')
                    users.save()

                # Email aendern und Log eintrag dazu erstellen
                if request.POST.get('email') != '':
                    users.email = request.POST.get('email')
                    users.save()

                messages.success(request, 'Du hast erfolgreich deine Einstellungen geaendert!')
            except:
                messages.error(request, 'Deine Einstellungen konnten nicht geaendert werden!')

            # Seite neuladen
            return redirect('home')
        else:
            return render(request, 'sites/settings.html')

    else:
        return redirect('login')

def get_expire_date(hours=24*7):
    now = datetime.datetime.now()
    return now + datetime.timedelta(hours=hours)


def get_random_size():
    return random.randint(35, 40)


def token_generator(size=40, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))