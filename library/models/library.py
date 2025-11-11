from django.db import models


class Library(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название библиотеки")
    location = models.CharField(max_length=200, verbose_name="Адрес")
    site = models.URLField(null=True, blank=True, verbose_name="Сайт")

    class Meta:
        db_table = 'libraries'
        verbose_name = "Library"
        verbose_name_plural = "Libraries"
        ordering = ['name']

    def __str__(self):
        return self.name
