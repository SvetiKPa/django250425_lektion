from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from library.enums import Gender


class Author(models.Model):
    first_name = models.CharField(max_length=20, help_text="First name of the author", verbose_name="Имя автора")
    last_name = models.CharField(max_length=50, help_text="Last name of the author", verbose_name="Фамилия автора")
    birthday = models.DateField(verbose_name="Дата рождения")
    profile =  models.URLField(blank=True, null=True, verbose_name="Ссылка на соцсеть")
    deleted = models.BooleanField(default=False, help_text="Если галочка включена автор удален", verbose_name="Профиль удален")
    rating = models.FloatField(
        validators=[MinValueValidator(0),
                    MaxValueValidator(10)],
        default=0,
        verbose_name="рейтинг автора"
    )

    class Meta:
        db_table = 'authors'
        verbose_name = "Author"
        verbose_name_plural = "Authors"
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.last_name[0]}.{self.first_name}"


class AuthorDetail(models.Model):
    author = models.OneToOneField(Author, on_delete=models.SET_NULL, null=True, related_name='details')
    biography = models.TextField(verbose_name="Биография")
    birth_city = models.CharField(max_length=50, verbose_name="Город рождения")
    gender = models.CharField(max_length=50, choices=Gender.choices(), null=True, blank=True, verbose_name="Пол")

    class Meta:
        db_table = 'author_details'
        verbose_name = "Author Detail"
        verbose_name_plural = "Author Details"

    def __str__(self):
        author_name = f"{self.author.last_name[0]}. {self.author.first_name}" if self.author else "N/A"
        return author_name
