from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Category(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 related_name='categories')
    tags = models.ManyToManyField(Tag, null=True, blank=True)
    title = models.CharField(max_length=50, null=True)
    id = models.IntegerField(primary_key=True)
    description = models.TextField()
    price = models.IntegerField(default=100)

    def __str__(self):
        return f"{self.description}: {self.price}"


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='reviews')
    id = models.IntegerField(primary_key=True)
    text = models.TextField()
    stars = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    def __str__(self):
        return f"{self.text}: {self.stars}"

