from django.contrib import admin
from .models import Author, Book, Product

admin.site.register([Author, Book, Product])
