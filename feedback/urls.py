from django.urls import path
from . import views

urlpatterns = [
	path('', views.queries_feedback_view, name='queries_feedback'),
	path('feedbacks/<int:pk>/', views.faculty_dashboard, name='faculty_feedback'),
	path('reply/<int:pk>/', views.reply_to_query, name='reply_to_query'),
	# path('feedback/', views.add_feedback, name='feedback')
]
