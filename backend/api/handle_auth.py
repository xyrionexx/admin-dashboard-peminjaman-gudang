from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view
from django import forms

class UserCredentialsForm(forms.form):
    email = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)
    remember_me = forms.BooleanField(required=False)

def validateUserCredentials(credentials):
    userForm = UserCredentialsForm(credentials)
    
    if not userForm.is_valid():
        return JsonResponse({
            'ErrMessage': "Maaf kayaknya di input kamu ada yang salah deh... Coba input lagi",
            "Error": userForm.errors
        }, status=400)
        
    return userForm

def register(request):
    userForm = validateUserCredentials(request.POST)
    
    # ambil user credentials
    email, password = map(lambda credential: userForm.cleaned_data.get(credential), ["email", "password"])

    # membuat objek user
    user = User.objects.create_user(username="", email=email, password=password)

    # simpan data user
    user.save()

def login(request):
    userForm = validateUserCredentials(request.POST)
        
    # ambil user credentials
    email, password, remember_me = map(lambda credential: userForm.cleaned_data.get(credential), ['email', 'password', 'remember_me'])

    # validasi user credentials
    user = authenticate(request, email=email, password=password)
    
    if not user:
        return JsonResponse({
            'errMessage': 'di input kamu ada yang salah nih...',
        }, status=400)
    
    # membuat sesi pengguna
    login(request, user)

    if remember_me:
        request.session.set_expiry(30 * 24 * 60 * 60) # set remember_me selama 30 hari
        
    return HttpResponse("Yay! Anda berhasil login :D", status=200)