from django.contrib import admin
from .models import FacultyProfile, StudentProfile

class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'reg_number', 'dept')
    search_fields = ('user__username', 'reg_number', 'dept')
    list_filter = ('dept',)

admin.site.register(StudentProfile, StudentProfileAdmin)

class FacultyProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'dept', 'phone_number', 'team_count')
    search_fields = ('user__username', 'dept')
    list_filter = ('dept', 'team_count')

admin.site.register(FacultyProfile, FacultyProfileAdmin)
