from django.db import models


class Publisher(models.Model):
    name = models.CharField(max_length=100, help_text="Name of the Publisher", verbose_name="Издательство")
    address = models.CharField(max_length=255, null=True, blank=True, verbose_name="Адрес")
    city = models.CharField(max_length=100, null=True, blank=True, verbose_name="Город")
    country = models.CharField(max_length=100, verbose_name="Страна")

    class Meta:
        db_table = 'publishers'
        verbose_name = "Publisher"
        verbose_name_plural = "Publishers"
        ordering = ['name']

    def __str__(self):
        return self.name
