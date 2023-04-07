# Define models
# The tables in the database

from django.db import models
from django.core.exceptions import ValidationError
from datetime import datetime

class Member(models.Model):
    # Fields
    first_name = models.TextField()
    last_name = models.TextField()
    email = models.EmailField()
    postcode = models.TextField()
    registration_date = models.DateField(default=datetime.now)

    # Validation
    def clean(self):
        if not all(str.isalpha(c) for c in self.first_name):
            raise ValidationError("Invalid firstname")

        if not all(str.isalpha(c) for c in self.last_name):
            raise ValidationError("Invalid lastname")

        if int(self.postcode) < 3000 or int(self.postcode) > 3999 or not self.postcode.isdigit():
            raise ValidationError("Invalid postcode")

    # User-friendly description
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Item(models.Model):
    # Fields
    name = models.TextField()
    price = models.FloatField()
    stock = models.IntegerField()

    # Validation
    def clean(self):
        if self.price < 0:
            raise ValidationError("Invalid price")

        if self.stock < 0:
            raise ValidationError("Invalid stock")

    # User-friendly description
    def __str__(self):
        return self.name

class Sale(models.Model):
    # Fields
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    item = models.ManyToManyField(Item)
    total = models.FloatField()
    date = models.DateField(default=datetime.now)

    # Validation
    def clean(self):
        if self.total < 0:
            raise ValidationError("Invalid cost")

    # User-friendly description
    def __str__(self):
        return f"{self.member} - ${self.total}"