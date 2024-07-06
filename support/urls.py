from django.urls import path
from . import views


urlpatterns = [
    path('', views.contact_admin, name='support'),
    path('success', views.success, name='success'),
]
