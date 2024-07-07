from django.urls import path
from . import views


urlpatterns = [
    path('student_dashboard', views.student_dashboard, name='student_dashboard'),
    path('upload_document/<int:project_id>/<str:document>/', views.upload_document, name='upload_document'),
    path('faculty_dashboard', views.faculty_dashboard, name='faculty_dashboard'),
    path('make_announcement/', views.make_announcement, name='make_announcement'),
    path('project_detail/<int:project_id>/', views.project_detail, name='project_detail'),
    path('upload_document/<int:project_id>/<str:document>/', views.upload_document, name='upload_document'),
    path('documents/<str:document_path>', views.document_view, name='document_view'),
    path('adjust_deadline/<int:project_id>/<str:document>/', views.adjust_deadline, name='adjust_deadline'),
    # path('approve_document/<int:project_id>/<str:document>/', views.approve_document, name='approve_document'),
    # path('reject_document/<int:project_id>/<str:document>/', views.reject_document, name='reject_document'),
    path('evaluate_document/<int:project_id>/<str:document>/', views.evaluate_document, name='evaluate_document'),
	path("plagarism_check",views.upload_and_check,name="upload_pdf"),
	path("plagarism_result/<int:pk>",views.plagiarism_result,name="plagiarism_result")
]
