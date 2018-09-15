from rest_framework import serializers
from api import models


class AudioSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Audio
        fields = (
            'name',
            'description'
        )


class SnippetSerializer(serializers.ModelSerializer):
    audio = AudioSerializer()

    class Meta:
        model = models.Snippet
        fields = (
            'audio',
            'start',
            'end',
            'url'
        )