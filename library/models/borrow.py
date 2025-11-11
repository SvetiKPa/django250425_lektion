from django.db import models
from django.utils import timezone


class Borrow(models.Model):
    member = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, related_name='borrows')
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True, related_name='borrows')
    library = models.ForeignKey('Library', on_delete=models.SET_NULL, null=True, related_name='borrows')
    borrow_date = models.DateField(verbose_name="Дата взятия книги")
    return_date = models.DateField(verbose_name="Дата возврата (планируемая)")
    actual_return_date = models.DateField(null=True, blank=True, verbose_name="Дата возврата (фактическая)")
    returned = models.BooleanField(default=False, verbose_name="Возвращена")

    class Meta:
        db_table = 'borrows'
        verbose_name = "Borrow"
        verbose_name_plural = "Borrows"
        ordering = ['-borrow_date']

    def __str__(self):
        book_title = self.book.title if self.book else "N/A"
        member_name = f"{self.member.last_name[0]}. {self.member.first_name}" if self.member else "N/A"
        return f"{book_title} - {member_name} ({self.borrow_date})"

    def is_overdue(self):
        if self.returned:
            return False
        return self.return_date < timezone.now().date()

    def was_returned_late(self):
        if not self.returned or not self.actual_return_date:
            return False
        return self.actual_return_date > self.return_date
