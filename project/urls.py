from django.urls import path
from . import views


urlpatterns = [
    path('student_dashboard', views.student_dashboard, name='student_dashboard'),
    path('upload_document/<int:project_id>/<str:document>/', views.upload_document, name='upload_document'),
    path('faculty_dashboard', views.faculty_dashboard, name='faculty_dashboard'),
    path('make_announcement/', views.make_announcement, name='make_announcement'),
]
