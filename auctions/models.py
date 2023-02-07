from email.policy import default
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.db import models
from datetime import datetime  


class User(AbstractUser):
    pass


class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=250)
    starting_bid = models.FloatField()
    url = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=64,blank=True, null=True)
    user = models.CharField(max_length=64)
    watchlist = models.ManyToManyField(User,blank=True, null=True, related_name="users_watching")
    highest = models.ForeignKey('Bid',blank=True, null=True, on_delete=models.SET_NULL)
    active = models.BooleanField(default=True)
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    # make users a user_id key 
    # make a boolen field and set active default to true
    
    def __str__(self):
        return f"{self.title}"
    
    
class Bid(models.Model):
    listings = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="items")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidders")
    bid = models.FloatField()
    



class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="item")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commenters")
    time = models.DateTimeField(default=datetime.now)
    comment = models.CharField(max_length=300)