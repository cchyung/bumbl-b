# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from api import signedurl

from api import models, serializers
from api.models import Snippet, Word, Audio


def sign_snippet(snippet):
    signed_url = signedurl.public_url(snippet['url'].replace("gs://", "https://storage.googleapis.com/"))

    signed_snippet = {
        'url': signed_url,
        'audio': snippet['audio'],
        'start': snippet['start'],
        'end': snippet['end']
    }

    return signed_snippet

@api_view(['GET'])
def create_snippet(request):
    try:
        word_object = Word.objects.get(value=request.GET.get("word"))
    except models.Word.DoesNotExist:
        word_object = Word(value=request.GET.get("word"))
        word_object.save()

    audio_object = Audio.objects.get(url=request.GET.get("rawUrl"))
    new_Snippet = Snippet(word=word_object, audio=audio_object, start=request.GET.get("starttime"), end=request.GET.get("endtime"), url=request.GET.get("url"))
    new_Snippet.save()

    print "Saved \"%s\" Snippet to database" % request.GET.get("word")
    """
    processes a sentence and returns an ordered list of snippets
    """
    response = "ok"
    return Response(response)



@api_view(['GET'])
def create_audio(request):
    audio = Audio(name=request.GET.get("name"), url=request.GET.get("url"), description=request.GET.get("description"))
    audio.save()
    print "Saved Audio \"%s\" to database" % audio
    """
    processes a sentence and returns an ordered list of snippets
    """
    response = "ok"
    return Response(response)


@api_view(['GET'])
def process(request):
    """
    processes a sentence and returns an ordered list of snippets
    """
    sentence = request.GET.get('query')
    words = sentence.split(" ")

    response = []

    for word in words:
        try:
            word_object = models.Word.objects.get(value=word)
        except models.Word.DoesNotExist:
            word_object = None

        if word_object is not None:
            snippet = models.Snippet.objects.filter(word=word_object).first()
            serializer = serializers.SnippetSerializer(snippet)

            signed_snippet = sign_snippet(serializer.data)

            response.append({'word': word, 'snippet': signed_snippet})
        else:
            response.append({'word': word, 'snippet': None})

    # return snippets
    return Response(response)


@api_view(['GET'])
def get_more_snippets(request):
    """
    gets another list of snippets that have this word
    """
    word = request.GET.get('query')

    response = []

    try:
        word_object = models.Word.objects.get(value=word)
    except models.Word.DoesNotExist:
        word_object = None

    if word_object is not None:
        snippets = models.Snippet.objects.filter(word=word_object)

        for snippet in snippets:
            serializer = serializers.SnippetSerializer(snippet)
            signed_snippet = sign_snippet(serializer.data)
            response.append(signed_snippet)

    # return snippets
    return (Response(
        response
    ))
