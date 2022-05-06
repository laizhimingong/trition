# Generated by Django 3.2.4 on 2021-06-28 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='user_info',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=50, verbose_name='用户名')),
                ('password', models.CharField(max_length=50, verbose_name='密码')),
                ('email', models.CharField(blank=True, max_length=50, verbose_name='邮箱')),
                ('phone', models.CharField(blank=True, max_length=20, verbose_name='手机号码')),
            ],
            options={
                'db_table': 'user_info',
                'ordering': ['id'],
            },
        ),
    ]
