from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('register/', views.register, name='register'),
    path('ask_login/', views.ask_login, name='ask_login'),
    path('student_login/', views.student_login, name='student_login'),
    path('faculty_login/', views.faculty_login, name='faculty_login'),
    path('join_team/', views.join_team, name='join_team'),
    path('team_selection/', views.team_selection, name='team_selection'),
    path('create_team/', views.create_team, name='create_team'),
    # path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
]
