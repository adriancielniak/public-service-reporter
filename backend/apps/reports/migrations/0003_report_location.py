# Generated migration for adding location fields to Report

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='latitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='report',
            name='longitude',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
