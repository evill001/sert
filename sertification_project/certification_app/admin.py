from django.contrib import admin
from .models import Profile, Document, Application

admin.site.register(Profile)
admin.site.register(Document)

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "created_at")
    list_filter = ("created_at",)
    search_fields = ("name", "email", "phone")