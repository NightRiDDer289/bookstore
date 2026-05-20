from django.db import models

class Category(models.Model):
  title = models.CharField(max_length=100)
  slug = models.SlugField(unique=True)
  description = models.CharField(max_length=200, blank=True, null=True)
  active = models.BooleanField(default=True)

  def __unicode__(self):
    return self.title
  
class Product(models.Model):
  title = models.CharField(max_length=255)
  description = models.TextField(max_length=500, blank=True, null=True)
  price = models.PositiveIntegerField(null=True)
  active = models.BooleanField(default=True)
  category = models.ManyToManyField(Category, blank=True)