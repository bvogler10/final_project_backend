# Generated by Django 5.1.3 on 2024-12-07 21:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project_app', '0009_inventoryitem_created_at_pattern_created_at'),
    ]

    operations = [
        migrations.DeleteModel(
            name='PatternImage',
        ),
    ]
