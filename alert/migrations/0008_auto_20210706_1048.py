# Generated by Django 3.2.4 on 2021-07-06 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alert', '0007_delete_userinfo'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='historyalert',
            options={'ordering': ['-startsAt']},
        ),
        migrations.RemoveField(
            model_name='historyalert',
            name='alerttype',
        ),
        migrations.AddField(
            model_name='historyalert',
            name='business',
            field=models.CharField(blank=True, max_length=20, verbose_name='业务'),
        ),
        migrations.AddField(
            model_name='historyalert',
            name='caltime',
            field=models.CharField(blank=True, max_length=80, verbose_name='异常时间'),
        ),
        migrations.AddField(
            model_name='historyalert',
            name='description',
            field=models.CharField(blank=True, max_length=1000, verbose_name='告警信息'),
        ),
        migrations.AddField(
            model_name='historyalert',
            name='endsAt',
            field=models.CharField(blank=True, max_length=80, verbose_name='告警恢复时间'),
        ),
        migrations.AddField(
            model_name='historyalert',
            name='env',
            field=models.CharField(blank=True, max_length=20, verbose_name='环境'),
        ),
        migrations.AddField(
            model_name='historyalert',
            name='fingerprint',
            field=models.CharField(blank=True, max_length=80, verbose_name='fingerprint'),
        ),
        migrations.AddField(
            model_name='historyalert',
            name='idc',
            field=models.CharField(blank=True, max_length=20, verbose_name='机房'),
        ),
        migrations.AddField(
            model_name='historyalert',
            name='instance',
            field=models.CharField(blank=True, max_length=50, verbose_name='实例'),
        ),
        migrations.AddField(
            model_name='historyalert',
            name='ip',
            field=models.CharField(blank=True, max_length=50, verbose_name='IP'),
        ),
        migrations.AddField(
            model_name='historyalert',
            name='port',
            field=models.CharField(blank=True, max_length=50, verbose_name='PORT'),
        ),
        migrations.AddField(
            model_name='historyalert',
            name='sendtime',
            field=models.CharField(blank=True, max_length=80, verbose_name='告警发送时间'),
        ),
        migrations.AddField(
            model_name='historyalert',
            name='severity',
            field=models.CharField(blank=True, max_length=20, verbose_name='告警级别'),
        ),
        migrations.AddField(
            model_name='historyalert',
            name='startsAt',
            field=models.CharField(blank=True, max_length=80, verbose_name='告警产生时间'),
        ),
        migrations.AddField(
            model_name='historyalert',
            name='status',
            field=models.CharField(blank=True, max_length=20, verbose_name='状态'),
        ),
        migrations.AddField(
            model_name='historyalert',
            name='summary',
            field=models.CharField(blank=True, max_length=1000, verbose_name='告警主旨'),
        ),
        migrations.AlterField(
            model_name='historyalert',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterModelTable(
            name='historyalert',
            table='history_alert',
        ),
    ]