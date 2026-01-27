from django.contrib import admin
from .models import Project, Task


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at', 'updated_at')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        (None, {
            'fields': ('title', 'description')
        }),
        ('状态信息', {
            'fields': ('status', 'result', 'notes')
        }),
        ('时间信息', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('project', 'title', 'completed', 'created_at')
    list_filter = ('completed', 'created_at')
    search_fields = ('project__title', 'title')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        (None, {
            'fields': ('project', 'title', 'description')
        }),
        ('任务状态', {
            'fields': ('completed',)
        }),
        ('时间信息', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )