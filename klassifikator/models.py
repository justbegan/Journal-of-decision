from django.db import models

class Region(models.Model):
    kod_regiona = models.IntegerField(unique=True)
    region = models.CharField(max_length=255)

    def __str__(self):
        return self.region

    class Meta:
        verbose_name = 'Регион'
        verbose_name_plural = 'Регионы'

class Raion(models.Model):
    region = models.ForeignKey(Region, on_delete=models.PROTECT)
    kod_raiona = models.IntegerField(unique=True)
    raion = models.CharField(max_length=255)

    def __str__(self):
        return str(self.kod_raiona) + ' ' + self.raion

    class Meta:
        verbose_name = 'Район'
        verbose_name_plural = 'Районы'