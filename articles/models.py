from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse
from django_ckeditor_5.fields import CKEditor5Field
from cloudinary.models import CloudinaryField


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def str(self):
        return self.name


class Article(models.Model):

    STATUS_CHOICES = (
        ('draft', 'draft'),
        ('published', 'published'),
    )

    # ✅ auteur
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="articles"
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="articles"
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='draft'
    )

    title = models.CharField(max_length=200)

    slug = models.SlugField(unique=True, blank=True)

    content = CKEditor5Field('content', config_name='default')

    # image cloudinary
    image = CloudinaryField(
        'image',
        folder='starmediablog/articles/images/',
        blank=True,
        null=True
    )
    # ❤️
    # 🎥 vidéo cloudinary
    video = CloudinaryField(
        'video',
        resource_type="video",
        folder='starmediablog/articles/videos/',
        blank=True,
        null=True
    )

    # 🎥 youtube optionnel
    youtube_id = models.CharField(max_length=50, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    views = models.PositiveIntegerField(default=0)


    def total_likes(self):
        return self.likes.count()

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('article_detail', kwargs={'slug': self.slug})

    def str(self):
        return self.title


# commentaires (déjà OK)
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

    def str(self):
        return f"comment by {self.name}"

class Like(models.Model):

    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name="likes"
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('article', 'user')

    def __str__(self):
        return f"{self.user.username} likes {self.article.title}"