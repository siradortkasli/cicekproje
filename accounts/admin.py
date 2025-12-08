from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "is_approved", "is_staff")
    list_filter = ("is_approved",)
    search_fields = ("username", "email")
