# Generated by Django 3.2.12 on 2022-02-12 23:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('back', '0016_remove_node_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='factory',
            name='icon',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='factory',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]