from django.db import models

# Create your models here.


class OpenWeatherToken(models.Model):
    name = models.CharField(verbose_name="name for token", max_length=64)
    token = models.CharField(verbose_name="token", max_length=128)
    cache = models.IntegerField(default=1, verbose_name="cache interval in min")

    def __str__(self) -> str:
        return f"{self.name}"
