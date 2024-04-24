from django.db import models

from .constant import NEW, CHOICES_STATUS, CHOICES_LEVEL


class Pereval(models.Model):

    status = models.CharField(max_length=10, choices=CHOICES_STATUS, default=NEW)
    beauty_title = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    other_titles = models.CharField(max_length=100)
    connect = models.CharField(max_length=100)
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='Time')

    user = models.ForeignKey('PerUser', on_delete=models.CASCADE)
    coords = models.ForeignKey('Cords', on_delete=models.CASCADE)
    level = models.ForeignKey('Level', on_delete=models.CASCADE)


class PerUser(models.Model):
    email = models.EmailField(unique=True, max_length=255)
    fam = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    otc = models.CharField(max_length=255)
    phone = models.CharField(unique=True)


class Cords(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    height = models.IntegerField()


class Level(models.Model):
    winter = models.CharField(max_length=2, choices=CHOICES_LEVEL, null=True, blank=True)
    summer = models.CharField(max_length=2, choices=CHOICES_LEVEL, null=True, blank=True)
    autumn = models.CharField(max_length=2, choices=CHOICES_LEVEL, null=True, blank=True)
    spring = models.CharField(max_length=2, choices=CHOICES_LEVEL, null=True, blank=True)


class Image(models.Model):

    data = models.ImageField()
    title = models.CharField(max_length=100)

    pereval = models.ForeignKey('Pereval', on_delete=models.CASCADE)