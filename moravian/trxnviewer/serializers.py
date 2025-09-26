from rest_framework import serializers
from .models import Memoir, MemoirImage, Transcription, Author


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name']


class TranscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transcription
        fields = ['id', 'text']


class MemoirImageSerializer(serializers.ModelSerializer):
    transcription = TranscriptionSerializer(read_only=True)

    class Meta:
        model = MemoirImage
        fields = ['id', 'page', 'image_url', 'transcription']


class MemoirSerializer(serializers.ModelSerializer):
    images = MemoirImageSerializer(many=True, read_only=True,
                                   source="visible_images")
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Memoir
        fields = ['id', 'author', 'start_date', 'end_date', 'date_precision',
                  'language', 'context_note', 'images']
