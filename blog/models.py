from django.db import models

# Create your models here.
from django.db  import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.html import strip_tags
import markdown
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
    #摘要
    excerpt = models.CharField(max_length=200, blank=True)
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

    def save(self, *args, **kwargs):
        #如果没有填写摘要
        if not self.excerpt:
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            #先将markdown文法渲染成html
            #strip_tags去掉html文本的全部标签
            #从文本摘取前54个字符赋值给excerpt
            self.excerpt = strip_tags(md.convert(self.body))[:54]
        super(Post, self).save(*args, **kwargs)
        