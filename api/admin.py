# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from api import models

from django.contrib import admin

# Register your models here.
admin.site.register(models.Audio)
admin.site.register(models.Snippet)
admin.site.register(models.Word)
