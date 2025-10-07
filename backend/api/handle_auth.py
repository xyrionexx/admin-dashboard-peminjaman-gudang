from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view
from django import forms

class UserCredentialsForm(forms.Form):
    username = forms.CharField(max_length=50, required=False)
    email = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)
    rememberMe = forms.BooleanField(required=False)

def validateUserCredentials(credentials):
    userForm = UserCredentialsForm(credentials)
    
    if not userForm.is_valid():
        raise Exception({
            'ErrMsg': 'Itu di input kamu kayak ada yang salah deh atau ngga sesuai',
            'Error': userForm.errors,
            'status': 400
        })
        
    return userForm

def register(request):
    try:
        userForm = validateUserCredentials(request.data)

        # Ambil user credentials
        username, email, password = map(
            lambda credential: userForm.cleaned_data.get(credential),
            ["username", "email", "password"]
        )

        # Membuat objek user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # Simpan data user
        user.save()

        return HttpResponse("Yay! akun mu berhasil dibuat :D", status=200)

    except Exception as e:
        return JsonResponse({
            'ErrMsg': str(e) if 'ErrMsg' not in e.__dict__ else e['ErrMsg'],
            'Error': str(e) if 'Error' not in e.__dict__ else e['Error']
        }, status=500 if 'status' not in e.__dict__ else e['status'])


def login(request):
    userForm = validateUserCredentials(request.data)
        
    # ambil user credentials
    credentials = ['username', 'email', 'password', 'rememberMe']
    username, email, password, remember_me = map(lambda credential: userForm.cleaned_data.get(credential), credentials)

    # validasi user credentials

    user = authenticate(request, username=username, email=email, password=password)
    
    if not user:
        return JsonResponse({
            'errMessage': 'di input kamu ada yang salah nih...',
        }, status=400)
    
    # membuat sesi pengguna
    auth_login(request, user)

    if remember_me:
        request.session.set_expiry(30 * 24 * 60 * 60) # set remember_me selama 30 hari
        
    return JsonResponse({
        'id': request.user.id,
        'username': request.user.username,
        'email': request.user.email
    }, status=200)