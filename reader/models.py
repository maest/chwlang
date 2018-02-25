from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)

class Article(models.Model):
    headline = models.CharField(max_length=500)
    body = models.TextField()
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.headline

    class Meta:
        ordering = ('headline',)
