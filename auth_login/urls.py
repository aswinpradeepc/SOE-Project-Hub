from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('register/', views.register, name='register'),
    path('ask_login/', views.ask_login, name='ask_login'),
    path('student_login/', views.student_login, name='student_login'),
    path('faculty_login/', views.faculty_login, name='faculty_login'),
    # path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
]
