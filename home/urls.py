from home import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('api/signup/', views.signup, name='signup'),
]
