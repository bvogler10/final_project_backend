# Generated by Django 5.1.3 on 2024-11-22 01:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_app', '0003_delete_project'),
    ]

    operations = [
        migrations.CreateModel(
            name='PatternImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pattern', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project_app.pattern')),
            ],
        ),
    ]
