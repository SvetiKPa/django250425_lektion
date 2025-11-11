from django.db import models


class Category(models.Model):
    name_category = models.CharField(
        max_length=30,
        unique=True,
        verbose_name="Имя категории"
    )

    class Meta:
        db_table = 'categories'
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['name_category']

    def __str__(self):
        return self.name_category
