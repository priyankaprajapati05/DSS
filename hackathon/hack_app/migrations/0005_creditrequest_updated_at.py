# Generated by Django 5.0.7 on 2025-04-05 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hack_app', '0004_alter_creditrequest_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='creditrequest',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
