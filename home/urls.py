from home import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('api/signup/', views.signup, name='signup'),
    path('api/category/<category_id>/', views.category_operations, name='category_operations'),
]
