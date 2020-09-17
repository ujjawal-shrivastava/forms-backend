from django.db import models
import uuid
from django.conf import settings
from datetime import datetime

def get_form_id():
    formid = str(uuid.uuid4().hex[:6])
    return formid

def get_response_id():
    responseid = str(uuid.uuid4().hex[:12])
    return responseid

class Form(models.Model):
    formid = models.CharField(primary_key=True, default=get_form_id, editable=False, max_length=6)
    title= models.CharField(max_length=100)
    description= models.CharField(max_length=100)
    isOpen= models.BooleanField()
    isPublished = models.BooleanField(default=False)
    bgtheme= models.CharField(max_length=7)
    data = models.TextField()
    views = models.PositiveIntegerField(default=0)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="forms", related_query_name="form")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Response(models.Model):
    responseid = models.CharField(primary_key=True, default=get_response_id, editable=False, max_length=12)
    data = models.TextField()
    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name="responses", related_query_name="response")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

