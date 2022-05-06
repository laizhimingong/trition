# Generated by Django 3.2.4 on 2021-08-13 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0015_delete_product'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('projectname', models.CharField(blank=True, max_length=40, verbose_name='所属产品')),
                ('createtime', models.CharField(blank=True, max_length=50, verbose_name='创建时间')),
                ('modifytime', models.CharField(blank=True, max_length=50, verbose_name='修改时间')),
            ],
            options={
                'db_table': 'Product',
            },
        ),
    ]
