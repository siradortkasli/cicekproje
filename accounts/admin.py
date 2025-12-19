from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "is_approved", "is_active", "is_staff")
    list_filter = ("is_approved", "is_active")
    search_fields = ("username", "email")
    actions = ["approve_users"]

    def approve_users(self, request, queryset):
        queryset.update(is_approved=True, is_active=True)

    approve_users.short_description = "Seçilen kullanıcıları onayla"
