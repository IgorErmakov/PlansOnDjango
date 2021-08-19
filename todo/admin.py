from django.contrib import admin
from .models import TodoItem

class TodoAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', )

admin.site.register(TodoItem, TodoAdmin)
