# Generated by Django 3.2.12 on 2022-02-11 23:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('back', '0008_auto_20220212_0433'),
    ]

    operations = [
        migrations.AddField(
            model_name='factorytype',
            name='danger_class',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='factory',
            name='factory_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='factory', to='back.factorytype'),
        ),
        migrations.AlterField(
            model_name='factory',
            name='phone',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
