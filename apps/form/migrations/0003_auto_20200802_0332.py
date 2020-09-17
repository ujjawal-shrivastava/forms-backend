# Generated by Django 3.0.8 on 2020-08-01 22:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('form', '0002_auto_20200802_0330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='form',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='forms', related_query_name='form', to=settings.AUTH_USER_MODEL),
        ),
    ]