from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils import timezone; timezone.now()
from django_ckeditor_5.fields import CKEditor5Field
from django.urls import reverse


class Category(models.Model):

    name = models.CharField(max_length=100)

    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Article(models.Model):

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="articles"
    )
    STATUS_CHOICES = (
        ('draft', 'draft'),
        ('published', 'published'),
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='draft'
    )

    title = models.CharField(max_length=200)

    slug = models.SlugField(unique=True, blank=True)

    content = CKEditor5Field('content')

    image = models.ImageField(upload_to="articles/", null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article_detail', kwargs={'slug': self.slug})






class Comment(models.Model):

    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name="comments"
    )

    name = models.CharField(max_length=100)
    email = models.EmailField()
    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"comment by {self.name}"

