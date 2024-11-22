from django.db import models

# Create your models here.
class Profile(models.Model):
    '''model for a user profile'''
    email = models.EmailField(blank=False)
    username = models.CharField(blank=False, max_length=50)
    first = models.CharField(blank=False, max_length=50)
    last = models.CharField(blank=False, max_length=50)
    bio = models.TextField(blank=True)
    link = models.URLField(blank=True)

    def __str__(self) -> str:
        return self.username

class InventoryItem(models.Model):
    '''model for an item in the user's inventory (e.g. yarn, needle, hook, stuffing)'''
    ITEM_TYPES = [
        ('yarn', 'Yarn'),
        ('hook_needle', 'Hook/Needles'),
        ('other', 'Other'),
    ]
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
    name = models.CharField(blank=False, max_length=100)
    item_type = models.CharField(max_length=20, choices=ITEM_TYPES)
    description = models.TextField(blank=True)
    image = models.ImageField(blank=True)

    def __str__(self) -> str:
        return self.name

class Pattern(models.Model):
    DIFFICULTY_TYPES = [
        ('beginner', 'Beginner'),
        ('advanced_beginner', 'Advanced Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert'),
    ]
    name = models.CharField(blank=False, max_length=75)
    creator = models.ForeignKey('Profile', on_delete=models.CASCADE)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_TYPES)
    description = models.TextField(blank=False)
    image = models.ImageField(blank=True)

    def __str__(self) -> str:
        return str(self.name) + ' Pattern'

class PatternImage(models.Model):
    '''images for patterns'''
    pattern = models.ForeignKey('Pattern', on_delete=models.CASCADE)
    image = models.ImageField(blank=True)

    def __str__(self) -> str:
        return str(self.pattern) + ' image'

class Post(models.Model):
    '''posts'''
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
    image = models.ImageField(blank=True)
    pattern = models.ForeignKey('Pattern', blank=True, null=True, on_delete=models.CASCADE)
    caption = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.profile) + 's post'

class SavedPattern(models.Model):
    '''saved patterns'''
    pattern = models.ForeignKey('Pattern', on_delete=models.CASCADE)
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return str(self.profile) + ' saved ' + str(self.pattern)

class SavedPost(models.Model):
    '''saved posts'''
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.profile) + ' saved ' + str(self.post)
    
class Like(models.Model):
    '''likes on posts'''
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.profile) + ' likes ' + str(self.post)

class Comment(models.Model):
    '''comments on posts'''
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
    comment = models.TextField(blank=True)

    def __str__(self) -> str:
        return str(self.profile) + ' commented on ' + str(self.post)

class Follow(models.Model):
    '''a following relationship'''
    follower = models.ForeignKey('Profile', on_delete=models.CASCADE,related_name='follower')
    following = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='following')

    def __str__(self) -> str:
        return str(self.follower) + ' follows ' + str(self.following)