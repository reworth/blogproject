from django.db import models

# Create your models here.
from django.db  import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.six import python_2_unicode_compatible

class Category(models.Model):
    """"
    继承models.Model类
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Tag(models.Model):
    """
    标签类
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Post(models.Model):
    """
    文章类
    """
    title = models.CharField(max_length=70)
    body = models.TextField()
    created_time = models.DateTimeField()
    modified_time = models.DateTimeField()
    category = models.ForeignKey(Category)
    #阅读量统计
    views = models.PositiveIntegerField(default=0)
    tags = models.ManyToManyField(Tag, blank=True)
    author = models.ForeignKey(User)


    def __str__(self):
        return self.title

##自定义get_absolute_url方法
    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-created_time']

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])
