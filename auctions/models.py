from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class User(AbstractUser):
    pass
    
    # Report structure
    def __str__(self):
        return f"{self.username}"

class categories(models.Model):
    listings_category = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.listings_category}"

    def format(self):
        return {'Category': self.listings_category}

class listings(models.Model):
    user_id = models.PositiveIntegerField()
    username = models.CharField(max_length=64)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=64)
    Starting_bid = models.DecimalField(max_digits=19, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    image_URL = models.URLField()
    category = models.CharField(max_length=64)
    closed = models.BooleanField(default=False)

    # Report structure
    def __str__(self):
        return f"{self.title}  {self.Starting_bid}  {self.category}"
    
    def format(self):
        return {
            "id": self.id, "user_id": self.user_id,"title": self.title, "description": self.description, "Starting_bid": self.Starting_bid, "image_URL": self.image_URL, "category": self.category, "closed": self.closed, "username": self.username
            }

class bids(models.Model):
    user_id = models.PositiveIntegerField()
    username = models.CharField(max_length=64)
    listing_id = models.PositiveIntegerField()
    bid_amount = models.DecimalField(max_digits=19, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])

    def __str__(self):
        return f"{self.id} @ {self.bid_amount}"
    
    def format(self):
        return {
            "id": self.id, "user_id": self.user_id,"username": self.username, "listing_id":self.listing_id, "bid_amount": self.bid_amount
            }

class comments(models.Model):
    user_id = models.PositiveIntegerField()
    username = models.CharField(max_length=64)
    listing_id = models.PositiveIntegerField()
    title = models.CharField(max_length=64)
    comment = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.comment}"
    
    def format(self):
        return {
            "id": self.id, "username": self.username, "title": self.title, "listing_id":self.listing_id, "comment": self.comment
            }

class Watchlist(models.Model):
    user_id = models.PositiveIntegerField()
    username = models.CharField(max_length=64)
    listing_id = models.PositiveIntegerField()
    listing_title = models.CharField(max_length=64)
    watched = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user_id} {self.username} {self.listing_id} {self.watched}"
    
    def format(self):
        return {
            "id": self.id, "user_id": self.user_id,"username": self.username, "listing_id":self.listing_id, "watched": self.watched, "title": self.listing_title
            }

    