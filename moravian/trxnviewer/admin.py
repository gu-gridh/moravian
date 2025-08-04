from django.contrib import admin
from django.utils.html import format_html
from .models import Author, MemoirImage, Memoir, Transcription


class MemoirInline(admin.TabularInline):
    extra = 0
    model = Memoir


class MemoirImageInline(admin.TabularInline):
    extra = 0
    model = MemoirImage


class TranscriptionInline(admin.TabularInline):
    extra = 0
    model = Transcription


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'updated']
    search_fields = ['name']
    readonly_fields = ['modified', 'updated']
    inlines = [
        MemoirInline
    ]


@admin.register(Memoir)
class MemoirAdmin(admin.ModelAdmin):
    list_display = ['author', 'language', 'start_date', 'end_date', 'updated']
    search_fields = ['author__name']
    readonly_fields = ['modified', 'updated']
    inlines = [
        MemoirImageInline
    ]


@admin.register(MemoirImage)
class MemoirImageAdmin(admin.ModelAdmin):
    list_display = ['page', 'image_url', 'updated']
    search_fields = ['memoir__author__name']
    readonly_fields = ['image_preview', 'modified', 'updated']
    inlines = [
        TranscriptionInline
    ]

    def image_preview(self, obj):
        if obj.image_url:
            return format_html('<img src="{}" style="max-width: 300px;" />',
                               obj.image_url)
        return "-"


@admin.register(Transcription)
class TranscriptionAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'updated']
    search_fields = ['text']
    fields = ['image_preview', 'text', 'image']
    readonly_fields = ['modified', 'updated', 'image_preview']

    def image_preview(self, obj):
        if obj.image.image_url:
            return format_html('<img src="{}" style="max-width: 300px;" />',
                               obj.image.image_url)
        return "-"
