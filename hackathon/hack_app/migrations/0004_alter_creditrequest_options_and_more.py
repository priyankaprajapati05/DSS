# Generated by Django 5.0.7 on 2025-04-05 09:43

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hack_app', '0003_rename_requested_at_creditrequest_timestamp_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='creditrequest',
            options={'ordering': ['-timestamp']},
        ),
        migrations.AlterModelOptions(
            name='uploadeddocument',
            options={'ordering': ['-uploaded_at']},
        ),
        migrations.AlterField(
            model_name='creditrequest',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='credit_requests', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='uploadeddocument',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documents', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='credits',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL),
        ),
    ]
