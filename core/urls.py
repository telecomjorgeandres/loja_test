from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
        path('', views.home, name='home'),
        path('register/', views.register, name='register'),
         # MODIFIED: Added redirect_authenticated_user=True to explicitly force redirection
        path('login/', auth_views.LoginView.as_view(template_name='core/login.html', redirect_authenticated_user=True), name='login'),
        path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    ]
