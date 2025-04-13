from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.

def index(request):
    return HttpResponse("Server is running")


@api_view(['POST'])
def signup(request):    
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    name = request.data.get('name') or ''
    
    if not username or not email or not password:
        return Response({'error': 'Please provide username, email and password'}, 
                        status=status.HTTP_400_BAD_REQUEST)
    
    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, 
                        status=status.HTTP_400_BAD_REQUEST)
    
    if User.objects.filter(email=email).exists():
        return Response({'error': 'Email already exists'}, 
                        status=status.HTTP_400_BAD_REQUEST)
    
    user = User.objects.create_user(
        first_name=name,
        username=username,
        email=email,
        password=password
    )
    
    refresh = RefreshToken.for_user(user)
    
    return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'name': user.first_name
        }
    }, status=status.HTTP_201_CREATED)
