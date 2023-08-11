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
from django.urls import reverse
from .models import OnetimePassword, OnetimeMessage


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
        try:
            user = User.objects.get(username=request.user.username)
            messages = OnetimeMessage.objects.filter(creator=user)
            passwords = OnetimePassword.objects.filter(creator=user)
        except Exception as e:
            error_message = str(e)
            dates = {'error_message': error_message}
            return render(request, 'sites/error.html', dates)
        all_models = []
        today = datetime.date.today()
        for message in messages:
            if message.opend:
                status = 'opend'
            elif today > message.token_expiry_date:
                status = 'expired'
            else:
                status = 'unopend'
            dic = {
                'id': message.id,
                'link_type': 'message',
                'name': message.name,
                'name_of_opener': message.name_of_opener,
                'url': request.build_absolute_uri(reverse('share_by_token', args=[message.one_time_token])),
                'status': status,
                'token_expiry_date': message.token_expiry_date,
                'date': message.update_date,
                'edit_url': request.build_absolute_uri(reverse('edit_by_id', args=['message', message.id])),
            }
            all_models.append(dic)
            
        for password in passwords:
            if password.opend:
                status = 'opend'
            elif today > password.token_expiry_date:
                status = 'expired'
            else:
                status = 'unopend'
            dic = {
                'id': password.id,
                'link_type': 'password',
                'name': password.name,
                'name_of_opener': password.name_of_opener,
                'url': request.build_absolute_uri(reverse('share_by_token', args=[password.one_time_token])),
                'status': status,
                'token_expiry_date': password.token_expiry_date,
                'date': password.update_date,
                'edit_url': request.build_absolute_uri(reverse('edit_by_id', args=['password', password.id])),
            }
            all_models.append(dic)

        all_models.sort(key=lambda x: x.get('date'), reverse=True)
        dates = {'all_models': all_models}
        if request.method == 'POST':
            if 'duplicate' in request.POST:
                value = request.POST.get('duplicate')
                value_list = value.split('-')
                link_type = value_list[0]
                identifier = value_list[1]
                if link_type == 'password':
                    try:
                        onetime_password = OnetimePassword.objects.get(id=identifier)

                        name = request.POST.get('name')
                        share_username = onetime_password.username
                        password = onetime_password.password
                        creator = onetime_password.creator
                        one_time_token = token_generator(size=get_random_size())
                        token_expiry_date = datetime.datetime.strptime(request.POST.get('token_expiry_date'), "%Y-%m-%d").date()

                        new_onetime_password = OnetimePassword(
                            name=name, username=share_username, password=password,
                            creator=creator, one_time_token=one_time_token,
                            token_expiry_date=token_expiry_date
                        )
                        new_onetime_password.save()

                        return redirect('show_link_by_id', link_type='password', identifier=new_onetime_password.id)
                    except Exception as e:
                        error_message = str(e)
                        dates = {'error_message': error_message}
                        return render(request, 'sites/error.html', dates)
                
                elif link_type == 'message':
                    try:
                        onetime_message = OnetimeMessage.objects.get(id=identifier)

                        name = request.POST.get('name')
                        message = onetime_message.message
                        creator = onetime_message.creator
                        one_time_token = token_generator(size=get_random_size())
                        token_expiry_date = datetime.datetime.strptime(request.POST.get('token_expiry_date'), "%Y-%m-%d").date()

                        new_onetime_message = OnetimeMessage(
                            name=name, message=message,
                            creator=creator, one_time_token=one_time_token,
                            token_expiry_date=token_expiry_date
                        )
                        new_onetime_message.save()

                        return redirect('show_link_by_id', link_type='message', identifier=new_onetime_message.id)
                    except Exception as e:
                        error_message = str(e)
                        dates = {'error_message': error_message}
                        return render(request, 'sites/error.html', dates)

                else:
                    return redirect('home')

            elif 'delete' in request.POST:
                try:
                    value = request.POST.get('delete')
                    value_list = value.split('-')
                    link_type = value_list[0]
                    identifier = value_list[1]
                    if link_type == 'password':
                        onetime_link = OnetimePassword.objects.get(id=identifier)
                        onetime_link.delete()
                    elif link_type == 'message':
                        onetime_link = OnetimeMessage.objects.get(id=identifier)
                        onetime_link.delete()
                    else:
                        redirect('home')
                    
                    return redirect('home')
                except Exception as e:
                    error_message = str(e)
                    dates = {'error_message': error_message}
                    return render(request, 'sites/error.html', dates)

        else:
            return render(request, 'sites/home.html', dates)

    else:
        return redirect('login')
    

def edit_by_id(request, link_type, identifier):
    if request.user.is_authenticated:
        try:
            user = User.objects.get(username=request.user.username)
            if link_type == 'password':
                onetime_link = OnetimePassword.objects.get(id=identifier)
            elif link_type == 'message':
                onetime_link = OnetimeMessage.objects.get(id=identifier)
            else:
                redirect('home')
        except Exception as e:
            error_message = str(e)
            dates = {'error_message': error_message}
            return render(request, 'sites/error.html', dates)
        
        if onetime_link.creator == user:
            token_link = request.build_absolute_uri(reverse('share_by_token', args=[onetime_link.one_time_token]))
            dates = {
                'onetime_link': onetime_link,
                'token_link': token_link,
                'link_type': link_type,
            }
            if request.method == 'POST':
                try:
                    if request.POST.get('name') != '':
                        onetime_link.name = request.POST.get('name')
                        onetime_link.save()

                    if request.POST.get('token_expiry_date') != '':
                        onetime_link.token_expiry_date = datetime.datetime.strptime(request.POST.get('token_expiry_date'), "%Y-%m-%d").date()
                        onetime_link.save()

                    if request.POST.get('opend') == 'checked':
                        onetime_link.opend = True
                        onetime_link.save()
                    else:
                        onetime_link.opend = False
                        onetime_link.save()
                    
                    onetime_link.name_of_opener = request.POST.get('name_of_opener')
                    onetime_link.save()
                    
                    if link_type == 'password':
                        if request.POST.get('username') != '':
                            onetime_link.username = request.POST.get('username')
                            onetime_link.save()
                        
                        if request.POST.get('password') != '':
                            onetime_link.password = request.POST.get('password')
                            onetime_link.save()
                    
                    elif link_type == 'message':
                        if request.POST.get('message') != '':
                            onetime_link.message = request.POST.get('message')
                            onetime_link.save()

                    messages.success(request, 'Du hast erfolgreich den Link bearbeitet!')
                    return redirect('home')
                
                except Exception as e:
                    messages.error(request, 'Der Link konnten nicht bearbeitet werden! ('+ str(e) +')')
                    return redirect('edit_by_id', link_type=link_type, identifier=identifier)
                
            else:
                return render(request, 'sites/edit_by_id.html', dates)
        else:
            redirect('home')

    else:
        return redirect('login')


def base(request):
    if request.user.is_authenticated:
        dates = {}
        return render(request, 'base.html', dates)

    else:
        return redirect('login')
    

def new_password(request):
    if request.user.is_authenticated:
        now = datetime.datetime.now()
        dates = {
            'now': now,
        }

        if request.method == 'POST':
            try:
                user = User.objects.get(username=request.user.username)

                name = request.POST.get('name')
                share_username = request.POST.get('username')
                password = request.POST.get('password')
                creator = user
                one_time_token = token_generator(size=get_random_size())
                token_expiry_date = datetime.datetime.strptime(request.POST.get('token_expiry_date'), "%Y-%m-%d").date()

                new_onetime_password = OnetimePassword(
                    name=name, username=share_username, password=password,
                    creator=creator, one_time_token=one_time_token,
                    token_expiry_date=token_expiry_date
                )
                new_onetime_password.save()

                return redirect('show_link_by_id', link_type='password', identifier=new_onetime_password.id)
            
            except Exception as e:
                    messages.error(request, 'Der Link konnten nicht erstellt werden! ('+ str(e) +')')
                    return redirect('new_password')

        return render(request, 'sites/new_password.html', dates)

    else:
        return redirect('login')
        

def new_message(request):
    if request.user.is_authenticated:
        now = datetime.datetime.now()
        dates = {
            'now': now,
        }
        if request.method == 'POST':
            try:
                user = User.objects.get(username=request.user.username)

                name = request.POST.get('name')
                message = request.POST.get('message')
                creator = user
                one_time_token = token_generator(size=get_random_size())
                token_expiry_date = datetime.datetime.strptime(request.POST.get('token_expiry_date'), "%Y-%m-%d").date()

                new_onetime_message = OnetimeMessage(
                    name=name, message=message,
                    creator=creator, one_time_token=one_time_token,
                    token_expiry_date=token_expiry_date
                )
                new_onetime_message.save()

                return redirect('show_link_by_id', link_type='message', identifier=new_onetime_message.id)
            
            except Exception as e:
                    messages.error(request, 'Der Link konnten nicht erstellt werden! ('+ str(e) +')')
                    return redirect('new_message')

        return render(request, 'sites/new_message.html', dates)

    else:
        return redirect('login')
    

def share_by_token(request, token):
    try:
        onetime_link = OnetimePassword.objects.get(one_time_token=token)
        status = 'password_link_aviable'
    except:
        status = 'link_not_aviable'
    
    if status == 'link_not_aviable':
        try:
            onetime_link = OnetimeMessage.objects.get(one_time_token=token)
            status = 'message_link_aviable'
        except:
            dates = {'status': status}
            return render(request, 'sites/share_by_token.html', dates)
    
    token_expiry_date = onetime_link.token_expiry_date
    open_status = onetime_link.opend
    now = datetime.date.today()

    if now <= token_expiry_date and open_status == False:
        if status == 'password_link_aviable':
            if request.method == 'POST':
                opener = request.POST.get('name')
                status = 'password_link_aviable_and_open'

                try:
                    onetime_link.opend = True
                    onetime_link.name_of_opener = opener
                    onetime_link.save()
                except:
                    dates = {'status': 'server_error'}
                    return render(request, 'sites/share_by_token.html', dates)


                dates = {'status': status,
                        'name': onetime_link.name,
                        'share_username': onetime_link.username,
                        'password': onetime_link.password
                        }
                return render(request, 'sites/share_by_token.html', dates)
            else:
                dates = {'status': status,
                        'name': onetime_link.name,
                        }
                return render(request, 'sites/share_by_token.html', dates)
        
        elif status == 'message_link_aviable':
            if request.method == 'POST':
                opener = request.POST.get('name')
                status = 'message_link_aviable_and_open'

                try:
                    onetime_link.opend = True
                    onetime_link.name_of_opener = opener
                    onetime_link.save()
                except:
                    dates = {'status': 'server_error'}
                    return render(request, 'sites/share_by_token.html', dates)

                dates = {'status': status,
                        'name': onetime_link.name,
                        'message': onetime_link.message
                        }
                return render(request, 'sites/share_by_token.html', dates)
            
            else:
                dates = {'status': status,
                        'name': onetime_link.name,
                        }
                return render(request, 'sites/share_by_token.html', dates)
            
    else:
        status = 'link_not_aviable_anymore'
        dates = {'status': status}
        return render(request, 'sites/share_by_token.html', dates)
    

def show_link_by_id(request, link_type, identifier):
    if request.user.is_authenticated:
        try:
            user = User.objects.get(username=request.user.username)
            if link_type == 'password':
                onetime_link = OnetimePassword.objects.get(id=identifier)
            elif link_type == 'message':
                onetime_link = OnetimeMessage.objects.get(id=identifier)
            else:
                redirect('home')
        except Exception as e:
            error_message = str(e)
            dates = {'error_message': error_message}
            return render(request, 'sites/error.html', dates)
        
        if onetime_link.creator == user:
            token_link = request.build_absolute_uri(reverse('share_by_token', args=[onetime_link.one_time_token]))
            dates = {
                'name': onetime_link.name,
                'token_link': token_link,
            }
            return render(request, 'sites/link_by_id.html', dates)
        
        else:
            redirect('home')

    else:
        return redirect('login')


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
            
            try:
                if request.POST.get('firstname') != '':
                    users.first_name = request.POST.get('firstname')
                    users.save()

                if request.POST.get('lastname') != '':
                    users.last_name = request.POST.get('lastname')
                    users.save()

                if request.POST.get('email') != '':
                    users.email = request.POST.get('email')
                    users.save()

                messages.success(request, 'Du hast erfolgreich deine Einstellungen geaendert!')
            except:
                messages.error(request, 'Deine Einstellungen konnten nicht geaendert werden!')

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