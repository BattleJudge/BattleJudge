# Generated by Django 3.1.5 on 2021-01-27 02:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20210124_2112'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='reset_email_token',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='reset_email_token_expire_time',
            field=models.DateTimeField(null=True),
        ),
    ]
