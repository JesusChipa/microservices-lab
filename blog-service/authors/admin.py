from django.contrib import admin
from .models import Author


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['display_name', 'email', 'created_at']
    search_fields = ['display_name', 'email']
