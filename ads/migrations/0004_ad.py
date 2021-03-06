# Generated by Django 3.1.5 on 2021-01-10 20:26

import ads.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ads', '0003_city'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('name', models.CharField(max_length=200, verbose_name='Название объявления')),
                ('description', models.TextField(verbose_name='Описание')),
                ('publication_date', models.DateTimeField(verbose_name='Дата публикации')),
                ('price', ads.models.MoneyField(decimal_places=2, max_digits=16, verbose_name='Стоимость')),
                ('status', models.PositiveSmallIntegerField(choices=[(1, 'Черновик'), (2, 'На модерации'), (3, 'Отклонено'), (4, 'Снято / продано'), (5, 'Активно')], verbose_name='Статус объявления')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ads', to='ads.category', verbose_name='Категория объявления')),
                ('city', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ads', to='ads.city', verbose_name='Город')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ads', to=settings.AUTH_USER_MODEL, verbose_name='Продавец')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
