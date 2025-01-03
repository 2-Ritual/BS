# Generated by Django 2.2 on 2024-12-25 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=255, verbose_name='产品名称')),
                ('price_1', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='价格')),
                ('price_2', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='价格')),
                ('price_3', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='价格')),
                ('price_4', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='价格')),
                ('price_5', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='价格')),
                ('price_6', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='价格')),
                ('price_7', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='价格')),
                ('price_8', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='价格')),
                ('price_9', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='价格')),
                ('price_10', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='价格')),
                ('price_11', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='价格')),
                ('price_12', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='价格')),
                ('product_url', models.URLField(max_length=511, verbose_name='产品链接')),
                ('image', models.URLField(unique=True, verbose_name='图片URL')),
                ('origin', models.CharField(blank=True, max_length=255, null=True, verbose_name='产地')),
                ('tags', models.CharField(blank=True, max_length=255, null=True, verbose_name='标签')),
                ('tags_info', models.TextField(blank=True, null=True, verbose_name='标签信息')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=150, unique=True, verbose_name='用户名')),
                ('password', models.CharField(max_length=128, verbose_name='密码')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='电子邮件')),
            ],
        ),
    ]
