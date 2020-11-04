# Generated by Django 2.2 on 2020-09-27 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=64, verbose_name='город')),
                ('phone', models.PositiveSmallIntegerField(verbose_name='телефон')),
                ('email', models.CharField(max_length=64, verbose_name='адрес электронной почты')),
                ('address', models.CharField(max_length=128, verbose_name='адрес')),
            ],
            options={
                'verbose_name': 'магазин',
                'verbose_name_plural': 'магазины',
            },
        ),
    ]