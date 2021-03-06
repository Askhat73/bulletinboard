# Generated by Django 3.1.5 on 2021-01-10 20:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ads', '0005_photo'),
    ]

    operations = [
        migrations.CreateModel(
            name='ModerationEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('decision', models.PositiveSmallIntegerField(choices=[(1, 'Опубликовать'), (2, 'Отправить на доработку')], verbose_name='Статус объявления')),
                ('reason', models.CharField(max_length=200, verbose_name='Причина отклонения к доработке')),
                ('ad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='moderation_entry', to='ads.ad', verbose_name='Объявление')),
                ('moderator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='moderation_entries', to=settings.AUTH_USER_MODEL, verbose_name='Модератор')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
