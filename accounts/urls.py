from django.urls import path
from . import views

urlpatterns = [
    # វាយលីង: /accounts/login/
    path('login/', views.login_view, name='login'),
    
    # វាយលីង: /accounts/register/
    path('register/', views.register_view, name='register'),
    
    # វាយលីង: /accounts/logout/
    path('logout/', views.logout_view, name='logout'),
]