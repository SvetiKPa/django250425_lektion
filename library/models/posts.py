from django.db import models


class Posts(models.Model):
    title = models.CharField(max_length=255, unique_for_date='created_at', verbose_name="Заголовок")
    body = models.TextField(verbose_name="Содержание")
    author = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, related_name='posts')
    moderated = models.BooleanField(default=False, verbose_name="Модерировано")
    library = models.ForeignKey('Library', on_delete=models.SET_NULL, null=True, related_name='posts')
    created_at = models.DateField(verbose_name="Дата создания")
    updated_at = models.DateField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        db_table = 'posts'
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        ordering = ['-created_at']

    def __str__(self):
        return self.title
