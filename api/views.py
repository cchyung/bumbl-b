# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist

from api import models, serializers


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
            response.append({'word': word, 'snippet': serializer.data})
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

    try:
        word_object = models.Word.objects.get(value=word)
    except models.Word.DoesNotExist:
        word_object = None

    if word_object is not None:
        snippets = models.Snippet.objects.filter(word=word_object)
        serializer = serializers.SnippetSerializer(snippets, many=True)
        response = serializer.data
    else:
        response = []

    # return snippets
    return (Response(
        {'snippets': response}
    ))