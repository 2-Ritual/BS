from django.db import models


class User(models.Model):
    username = models.CharField(max_length=150, unique=True, verbose_name='用户名')
    password = models.CharField(max_length=128, verbose_name='密码')
    email = models.EmailField(unique=True, verbose_name='电子邮件')

    def __str__(self):
        return self.username


class Product(models.Model):
    product_name = models.CharField(max_length=255, verbose_name='产品名称')
    price_1 = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='价格', default=0)
    price_2 = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='价格', default=0)
    price_3 = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='价格', default=0)
    price_4 = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='价格', default=0)
    price_5 = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='价格', default=0)
    price_6 = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='价格', default=0)
    price_7 = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='价格', default=0)
    price_8 = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='价格', default=0)
    price_9 = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='价格', default=0)
    price_10 = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='价格', default=0)
    price_11 = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='价格', default=0)
    price_12 = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='价格', default=0)

    product_url = models.URLField(max_length=511, verbose_name='产品链接')
    image = models.URLField(verbose_name='图片URL', unique=True)
    origin = models.CharField(max_length=255, verbose_name='产地', null=True, blank=True)
    tags = models.CharField(max_length=255, verbose_name='标签', null=True, blank=True)
    tags_info = models.TextField(verbose_name='标签信息', null=True, blank=True)

    def __str__(self):
        return self.product_name

