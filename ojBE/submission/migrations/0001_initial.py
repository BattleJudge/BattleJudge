# Generated by Django 3.1.5 on 2021-02-18 14:48

from django.db import migrations, models
import django.db.models.deletion
import django_mysql.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('problem', '0002_solution'),
    ]

    operations = [
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('user_id', models.IntegerField(db_index=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('code', models.TextField()),
                ('result', models.IntegerField(db_index=True, default=6)),
                ('info', django_mysql.models.JSONField(default=dict)),
                ('static_info', django_mysql.models.JSONField(default=dict)),
                ('language', models.TextField()),
                ('pro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='problem.problem')),
            ],
            options={
                'db_table': 'submission',
            },
        ),
    ]
