# Generated by Django 5.1.3 on 2024-11-30 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_app', '0005_alter_post_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]