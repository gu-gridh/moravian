from django.contrib import admin
from .models import Author, MemoirImage, Memoir, Transcription


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'updated']
    readonly_fields = ['modified', 'updated']


@admin.register(Memoir)
class MemoirAdmin(admin.ModelAdmin):
    list_display = ['author', 'language', 'start_date', 'end_date', 'updated']
    readonly_fields = ['modified', 'updated']


@admin.register(MemoirImage)
class MemoirImageAdmin(admin.ModelAdmin):
    list_display = ['page', 'image_url', 'updated']
    readonly_fields = ['modified', 'updated']


@admin.register(Transcription)
class TranscriptionAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'updated']
    readonly_fields = ['modified', 'updated']
