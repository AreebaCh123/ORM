from django.db import models

# Custom Manager
class StudentManager(models.Manager):
    def adults(self):
        return self.filter(age__gte=18)


class Student(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()

    # Attach the custom manager
    objects = StudentManager()

    def __str__(self):
        return self.name
