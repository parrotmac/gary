# Generated by Django 4.0 on 2021-12-22 04:46

from django.db import migrations, models
import gifter.models


class Migration(migrations.Migration):

    dependencies = [
        ('gifter', '0003_groupinvitation_http_origin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupinvitation',
            name='verification_code',
            field=models.CharField(default=gifter.models.verification_code, editable=False, max_length=32),
        ),
    ]
