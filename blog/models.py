# Create your models here.

from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify


class PostManager(models.Manager):
    def live(self):
        return self.model.objects.filter(published=True)


class Post(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    topic_tag = models.CharField(max_length=255) # make sure to add this elsewhere
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, blank=True, default='')
    short_descr = models.CharField(max_length=255) # due diligence
    content = models.TextField()
    published = models.BooleanField(default=True)
    author = models.ForeignKey(User, related_name="posts")
    ttr = models.CharField(max_length=255) # due diligence
    objects = PostManager()

    class Meta:
        ordering = ["-created_at", "title"]

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return ("blog:detail", (), {"slug": self.slug})
