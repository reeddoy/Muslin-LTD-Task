from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.text import slugify
from home.models import *
from home.serializer import *
import uuid
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


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def category_operations(request, category_id):
    # GET - Get all categories
    if request.method == 'GET':
        categories = Product_Category.objects.all()
        serializer = ProductCategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # POST - Create a new category
    elif request.method == 'POST':
        # Get data directly from request
        name = request.data.get('name')
        # Generate slug from name
        slug = slugify(name)
        
        # Validate required fields
        if not name:
            return Response({'error': 'Name is required'}, 
                            status=status.HTTP_400_BAD_REQUEST)
        
        # Check if slug already exists
        if Product_Category.objects.filter(slug=slug).exists():
            slug = slugify(name) + '-' + str(uuid.uuid4())[:8]
            
        store = Product_Category.objects.create(name=name, slug=slug)
        serializer = ProductCategorySerializer(store)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    
    # Try to get the category for PUT and DELETE operations
    if request.method in ['PUT', 'DELETE']:
        try:
            category = Product_Category.objects.get(id=category_id)
        except Product_Category.DoesNotExist:
            return Response({'error': 'Category not found'}, 
                            status=status.HTTP_404_NOT_FOUND)
    
        # PUT - Update a category
        if request.method == 'PUT':
            try:
                name = request.data.get('name')
                category.name = name
                category.save()
                serializer = ProductCategorySerializer(category)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        
        # DELETE - Delete a category
        elif request.method == 'DELETE':
            try:
                category.delete()
                return Response({'message': 'Category deleted successfully'}, 
                                status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



