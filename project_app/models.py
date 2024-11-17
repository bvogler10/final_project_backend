from django.db import models

# Create your models here.
class Profile(models.Model):
    '''model for a user profile'''
    email = models.TextField(blank=False)
    username = models.TextField(blank=False)
    first = models.TextField(blank=False)
    last = models.TextField(blank=False)
    bio = models.TextField(blank=True)
    link = models.URLField(blank=True)

class InventoryItem(models.Model):
    '''model for an item in the user's inventory (e.g. yarn, needle, hook, stuffing)'''
    ITEM_TYPES = [
        ('yarn', 'Yarn'),
        ('hook_needle', 'Hook/Needles'),
        ('other', 'Other'),
    ]
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
    name = models.TextField(blank=False)
    item_type = models.CharField(max_length=20, choices=ITEM_TYPES)
    description = models.TextField(blank=True)

class Pattern(models.Model):
    DIFFICULTY_TYPES = [
        ('beginner', 'Beginner'),
        ('advanced_beginner', 'Advanced Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert'),
    ]
    name = models.TextField(blank=False)
    creator = models.ForeignKey('Profile', on_delete=models.CASCADE)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_TYPES)
    description = models.TextField(blank=False)
    image = models.ImageField

class Project(models.Model):
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
    pattern = models.ForeignKey('Pattern', on_delete=models.CASCADE, blank=True)
    name = models.TextField(blank=False)
    notes = models.TextField(blank=True)

