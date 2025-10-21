from django.contrib import admin
from .models import Sprint, Story

# Register your models here.

@admin.register(Sprint)
class SprintAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "start_date", "end_date")
    search_fields = ("title",)
    ordering = ("start_date",)

@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "sprint", "updated_on")
    list_filter = ("status", "sprint")
    search_fields = ("title", "description")
    readonly_fields = ("created_on", "updated_on")