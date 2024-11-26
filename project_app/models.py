import uuid
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager

from django.db import models

# Create your models here.
class CustomUserManager(UserManager):
    def _create_user(self, name, email, password, **extra_fields):
        if not email:
            raise ValueError("You have not specified a valid email address")
        
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)

        return user
    def create_user(self, name=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(name, email, password, **extra_fields)

    def create_superuser(self, name=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(name, email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    username = models.CharField(blank=False, max_length=50)
    bio = models.TextField(blank=True)
    link = models.URLField(blank=True)
    avatar = models.ImageField(blank=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['name','username',]

class InventoryItem(models.Model):
    '''model for an item in the user's inventory (e.g. yarn, needle, hook, stuffing)'''
    ITEM_TYPES = [
        ('yarn', 'Yarn'),
        ('hook_needle', 'Hook/Needles'),
        ('other', 'Other'),
    ]
    user = models.ForeignKey('User', on_delete=models.CASCADE)
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
    creator = models.ForeignKey('User', on_delete=models.CASCADE)
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
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    image = models.ImageField(blank=True)
    pattern = models.ForeignKey('Pattern', blank=True, null=True, on_delete=models.CASCADE)
    caption = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.user) + 's post'

class SavedPattern(models.Model):
    '''saved patterns'''
    pattern = models.ForeignKey('Pattern', on_delete=models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return str(self.user) + ' saved ' + str(self.pattern)

class SavedPost(models.Model):
    '''saved posts'''
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.user) + ' saved ' + str(self.post)
    
class Like(models.Model):
    '''likes on posts'''
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.user) + ' likes ' + str(self.post)

class Comment(models.Model):
    '''comments on posts'''
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    comment = models.TextField(blank=True)

    def __str__(self) -> str:
        return str(self.user) + ' commented on ' + str(self.post)

class Follow(models.Model):
    '''a following relationship'''
    follower = models.ForeignKey('User', on_delete=models.CASCADE,related_name='follower')
    following = models.ForeignKey('User', on_delete=models.CASCADE, related_name='following')

    def __str__(self) -> str:
        return str(self.follower) + ' follows ' + str(self.following)