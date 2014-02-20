import datetime
from django.db import models

# Create your models here.


class BlogAutors(models.Model):
    name = models.CharField(max_length=128)

    def __unicode__(self):
        return self.name


class BlogPosts(models.Model):
    label = models.CharField(max_length=256)
    content = models.TextField('It is your post.')
    publication_date = models.DateTimeField(default=datetime.datetime.now(),
                                            db_index=True)
    is_arhive = models.BooleanField(default=False, db_index=True)
    autor = models.ForeignKey(BlogAutors)

    def __unicode__(self):
        return self.label + ' - ' + str(self.publication_date)

    def is_publised(self):
        # Returns True if post create before this moment.
        return datetime.datetime.now() >= self.publication_date


class Comment(models.Model):
    email = models.EmailField()
    content = models.CharField(max_length=512)
    publication_date = models.DateTimeField(default=datetime.datetime.now(),
                                            db_index=True)
    is_hide = models.BooleanField(default=False, db_index=True)
    post_id = models.ForeignKey(BlogPosts)

    def __unicode__(self):
        return str(self.post_id) + ': ' + self.autor
