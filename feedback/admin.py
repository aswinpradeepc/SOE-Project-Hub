from django.contrib import admin

# Register your models here.
from .models import Query, Feedback

admin.site.register(Query)
admin.site.register(Feedback)
