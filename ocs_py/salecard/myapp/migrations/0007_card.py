# Generated by Django 3.2.20 on 2023-09-02 08:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('myapp', '0006_alter_userprofile_wechat_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_code', models.CharField(max_length=12, unique=True)),
                ('hash_value', models.CharField(max_length=32)),
                ('video_list', models.JSONField(default=list)),
                ('name', models.CharField(max_length=100)),
                ('avatar_url', models.URLField()),
                ('card_style_image_url', models.URLField()),
                ('card_rights', models.CharField(max_length=100)),
                ('boss', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bossed_cards', to=settings.AUTH_USER_MODEL)),
                ('manager', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='managed_cards', to=settings.AUTH_USER_MODEL)),
                ('salesman', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sold_cards', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sent_cards', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
