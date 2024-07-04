from django.urls import path
from . import views


urlpatterns = [
    path('student_dashboard', views.student_dashboard, name='student_dashboard'),
    path('upload_document/<int:project_id>/<str:document>/', views.upload_document, name='upload_document'),
]
