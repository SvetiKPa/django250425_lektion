from django.core.validators import MaxValueValidator
from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    publication_date = models.DateField(blank=True, null=True, verbose_name="Дата публикации")
    author = models.ForeignKey(
        "Author",
        on_delete=models.SET_NULL,
        null=True,
        related_name="books"
    )
    description = models.TextField(blank=True, null=True, verbose_name="Краткое описание")
    page_count = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(10_000)],
        blank=True, null=True, verbose_name="Страницы"
    )

    publisher = models.ForeignKey("Publisher", on_delete=models.SET_NULL, null=True, related_name="books" )

    category = models.ForeignKey(
        'Category',
        on_delete=models.PROTECT,
        related_name="books",
        null=True, blank=True,
        verbose_name="Категория")
    libraries = models.ManyToManyField('Library', related_name='books')
    contributor = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)

    @property
    def rating(self):
        reviews = self.reviews.all()
        total_reviews = reviews.count()

        if total_reviews == 0:
            return 0

        total_rating = sum(review.rating for review in reviews)
        average_rating = total_rating / total_reviews

        return round(average_rating, 2)

    class Meta:
        db_table = 'books'
        verbose_name = "Book"
        verbose_name_plural = "Books"
        ordering = ['title']


    def __str__(self):
        return f"{self.title} --{self.author.last_name if self.author else 'NONAME'}"
