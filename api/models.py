# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.
class Audio(models.Model):
    name = models.CharField(max_length=100, blank=False)
    url = models.URLField(max_length=300)
    description = models.CharField(max_length=500, blank=True)


class Word(models.Model):
    value = models.CharField(max_length=20, blank=False)


class Snippet(models.Model):
    word = models.ForeignKey(Word)
    audio = models.ForeignKey(Audio)
    start = models.IntegerField()
    end = models.IntegerField()
    url = models.URLField(max_length=300)
