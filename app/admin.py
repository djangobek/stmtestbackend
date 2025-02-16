from django.contrib import admin

# Register your models here.
from .models import *

@admin.register(BotUserModel)
class BotUserAdmin(admin.ModelAdmin):
    list_display = ['name','telegram_id','language','added']
    list_editable = ['language','name']
    list_display_links = ['telegram_id']
    list_per_page = 10
@admin.register(TelegramChannelModel)
class TelegramChannelAdmin(admin.ModelAdmin):
    list_display = ['channel_id','channel_name','channel_members_count']
    list_display_links = ['channel_name']
    list_per_page = 10

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "type", "count", "created",'owner','status')  # Columns displayed in the list view
    list_filter = ("type", "created","owner",'status')  # Filter sidebar for these fields
    search_fields = ("name", "code", "type",'owner')  # Search functionality
    readonly_fields = ("code", "created")  # Fields that are not editable
    ordering = ("-created",)  # Default ordering by creation date (descending)

    fieldsets = (
        (None, {
            "fields": ("name", "code", "answers", "type", "count",'owner','status'),
        }),
        ("Additional Info", {
            "fields": ("created",),
            "classes": ("collapse",),  # Collapsible section for additional info
        }),
    )

@admin.register(TestParticipation)
class TestParticipationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'test', 'participated_at', 'correct_answer', 'wrong_answer', 'certificate')
    list_filter = ('certificate', 'participated_at')
    search_fields = ('user__username', 'test__name', 'answers')
    date_hierarchy = 'participated_at'
    ordering = ('-participated_at',)
    readonly_fields = ('participated_at',)

    fieldsets = (
        (None, {
            'fields': ('user', 'test', 'answers', 'correct_answer', 'wrong_answer', 'certificate')
        }),
        ('Participation Info', {
            'fields': ('participated_at',),
            'classes': ('collapse',),
        }),
    )


@admin.register(FileCollection)
class FileCollectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'id')  # Show these fields in the list
    search_fields = ('title',)  # Enable search by title
    list_filter = ('title',)  # Add filtering option
    fields = ('title', 'file_ids', 'description')  # Fields to show in edit page

    def formatted_file_ids(self, obj):
        """
        Format file_ids as a readable JSON string
        """
        return "\n".join(obj.file_ids) if obj.file_ids else "No files"

    formatted_file_ids.short_description = "File IDs"