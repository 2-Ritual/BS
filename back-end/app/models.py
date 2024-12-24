from django.db import models


# Create your models here.
class MailVerify(models.Model):
    objects = models.Manager()
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=4)
    email = models.CharField(max_length=45, unique=True)

    @classmethod
    def create_mail_verify(cls, code, email):
        mail_verify = cls(code=code, email=email)
        mail_verify.save()
        return mail_verify

    @classmethod
    def get_mail_verify(cls, email):
        try:
            mail_verify = cls.objects.get(email=email)
            return mail_verify
        except cls.DoesNotExist:
            return None


class User(models.Model):
    objects = models.Manager()
    uid = models.AutoField(primary_key=True)
    account = models.CharField(max_length=45, unique=True)
    state = models.IntegerField(default=0)
    password = models.CharField(max_length=64)
    email = models.CharField(max_length=45)
    name = models.CharField(max_length=45, null=True)
    mid = models.TextField(null=True)
    token = models.CharField(max_length=64, null=True)


class Tag(models.Model):
    objects = models.Manager()
    tid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)
    description = models.CharField(max_length=255, null=True)

    @classmethod
    def create_tag(cls, name, description):
        tag = cls(name=name, description=description)
        tag.save()
        return tag

    @classmethod
    def create_tags(cls, names, descriptions=None):
        tags = []
        for i in range(len(names)):
            if descriptions is None:
                description = None
            else:
                description = descriptions[i]
            tag = cls(name=names[i], description=description)
            tags.append(tag)
        cls.objects.bulk_create(tags)

    @classmethod
    def get_tags(cls):
        tags = cls.objects.all()
        return tags

    @classmethod
    def get_tag_by_id(cls, id):
        try:
            tag = cls.objects.get(id=id)
            return tag
        except cls.DoesNotExist:
            return None


class Mask(models.Model):
    objects = models.Manager()
    mid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)
    description = models.CharField(max_length=255, null=True)
    likes = models.TextField(null=True)
    dislikes = models.TextField(null=True)
    buf = models.TextField(null=True)
    user = models.ForeignKey("User", on_delete=models.CASCADE)


class Car(models.Model):
    objects = models.Manager()
    cid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)
    description = models.CharField(max_length=255)
    image = models.CharField(max_length=255, null=True)
    year = models.IntegerField()
    brand = models.CharField(max_length=45)
    model = models.CharField(max_length=45)
    price = models.FloatField()
    tags = models.CharField(max_length=100, null=True)
    # 12.10更新新增字段
    url = models.CharField(max_length=255, null=True)

    @classmethod
    def create_car(cls, name, description, image, year, brand, model, price, tags):
        car = cls(
            name=name,
            description=description,
            image=image,
            year=year,
            brand=brand,
            model=model,
            price=price,
        )
        car.save()
        car.tags.set(tags)
        return car

    @classmethod
    def create_cars(cls, cars):
        cls.objects.bulk_create(cars)

    @classmethod
    def get_cars(cls):
        cars = cls.objects.all()
        return cars
