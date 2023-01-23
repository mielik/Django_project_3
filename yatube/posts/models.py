from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200, verbose_name='Title of the group')
    slug = models.SlugField(unique=True, verbose_name="URL label")
    description = models.TextField(verbose_name='Description')

    def __str__(self) -> str:
        return self.title


class Post(models.Model):
    text = models.TextField(verbose_name='Text')
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Publication date'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL, null=True,
        related_name='posts',
        verbose_name='Author'
    )
    group = models.ForeignKey(
        Group,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Group'
    )

    def __str__(self) -> str:
        return (self.text)[:15]

    class Meta:
        ordering = ['-pub_date', ]
