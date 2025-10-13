from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view
from django import forms
from rest_framework_simplejwt.tokens import RefreshToken
import uuid
import datetime
from django.utils import timezone

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

# Session storage simulation
sessions = {}

@api_view(['POST'])
def create_session(request):
    """Create a new session for a user"""
    data = request.data
    token = data.get('token')
    user_id = data.get('userId')
    expires_at = data.get('expiresAt')
    
    if not all([token, user_id, expires_at]):
        return JsonResponse({'success': False, 'message': 'Missing required fields'}, status=400)
    
    # Store session
    sessions[token] = {
        'id': token,
        'userId': user_id,
        'expiresAt': expires_at
    }
    
    return JsonResponse({
        'success': True,
        'session': {'id': token, 'expiresAt': expires_at}
    })

@api_view(['POST'])
def validate_token(request):
    """Validate a session token"""
    token = request.data.get('token')
    
    if not token or token not in sessions:
        return JsonResponse({'valid': False}, status=401)
    
    session = sessions[token]
    expires_at = datetime.datetime.fromisoformat(session['expiresAt'].replace('Z', '+00:00'))
    
    # Check if session is expired
    if expires_at < timezone.now():
        del sessions[token]
        return JsonResponse({'valid': False, 'message': 'Session expired'}, status=401)
    
    # Get user data
    try:
        user = User.objects.get(id=session['userId'])
        
        return JsonResponse({
            'valid': True,
            'user': {
                'id': user.id,
                'username': user.username,
                'is_admin': user.is_staff or user.is_superuser
            },
            'expiresAt': session['expiresAt']
        })
    except User.DoesNotExist:
        return JsonResponse({'valid': False}, status=401)

@api_view(['POST'])
def renew_session(request):
    """Renew a session's expiration time"""
    token = request.data.get('token')
    expires_at = request.data.get('expiresAt')
    
    if not token or token not in sessions or not expires_at:
        return JsonResponse({'success': False, 'message': 'Invalid token or missing expiry'}, status=400)
    
    # Update expiration time
    sessions[token]['expiresAt'] = expires_at
    
    return JsonResponse({'success': True})

@api_view(['POST'])
def invalidate_session(request):
    """Invalidate (delete) a session"""
    token = request.data.get('token')
    
    if token and token in sessions:
        del sessions[token]
        
    return JsonResponse({'success': True})


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
        
    # Generate token
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    
    # Simpan token di session
    request.session['jwt_token'] = access_token
    request.session.save()

    return JsonResponse({
        'id': request.user.id,
        'username': request.user.username,
        'email': request.user.email,
        'is_admin': user.is_staff or user.is_superuser
    }, status=200)