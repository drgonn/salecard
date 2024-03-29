# Generated by Django 3.2.20 on 2023-09-03 09:37

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0011_hashvalue'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hashvalue',
            name='updated_at',
        ),
        migrations.AddField(
            model_name='application',
            name='application_arg',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='application',
            name='application_type',
            field=models.CharField(choices=[('注册公司', '注册公司'), ('添加员工', '添加员工'), ('申请批卡', '申请批卡')], default='添加员工', max_length=20),
        ),
        migrations.AddField(
            model_name='hashvalue',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='highest_role',
            field=models.CharField(default='普通人员', max_length=20),
        ),
        migrations.AlterField(
            model_name='hashvalue',
            name='hash_value',
            field=models.CharField(max_length=12),
        ),
        migrations.AlterField(
            model_name='hashvalue',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
