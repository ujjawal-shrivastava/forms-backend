# Generated by Django 3.0.8 on 2020-08-01 17:35

import apps.form.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Form',
            fields=[
                ('id', models.CharField(default=apps.form.models.get_form_id, editable=False, max_length=6, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=100)),
                ('isOpen', models.BooleanField()),
                ('isPublished', models.BooleanField(default=False)),
                ('bgtheme', models.CharField(max_length=7)),
                ('data', models.TextField()),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='forms', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]