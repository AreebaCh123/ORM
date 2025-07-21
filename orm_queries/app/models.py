from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=100)

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(active=True)

class Product(models.Model):
    name = models.CharField(max_length=100)
    active = models.BooleanField(default=True)

    objects = models.Manager()
    active_objects = ActiveManager()