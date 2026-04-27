from django.db import models


class Item(models.Model):
    """Пример модели"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Элемент'
        verbose_name_plural = 'Элементы'

    def __str__(self):
        return self.name
