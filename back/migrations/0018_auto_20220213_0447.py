# Generated by Django 3.2.12 on 2022-02-12 23:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('back', '0017_auto_20220213_0440'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='factory',
            name='factory_type',
        ),
        migrations.DeleteModel(
            name='FactoryType',
        ),
    ]