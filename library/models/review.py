from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Review(models.Model):
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True, related_name='reviews')
    reviewer = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, related_name='reviews')
    rating = models.FloatField(
        verbose_name="Рейтинг",
        validators=[MinValueValidator(0), MaxValueValidator(10)]
        )
    description = models.TextField(verbose_name="Описание")

    class Meta:
        db_table = 'reviews'
        verbose_name = "Review"
        verbose_name_plural = "Reviews"
        ordering = ['-rating']

    def __str__(self):
        book_title = self.book.title if self.book else "N/A"
        reviewer_name = f"{self.reviewer.last_name[0]}. {self.reviewer.first_name}" if self.reviewer else "N/A"
        return f"{book_title} - {reviewer_name} ({self.rating})"
 