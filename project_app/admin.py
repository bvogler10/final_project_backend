from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(User)
admin.site.register(InventoryItem)
admin.site.register(Pattern)
admin.site.register(PatternImage)
admin.site.register(Post)
admin.site.register(SavedPost)
admin.site.register(SavedPattern)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Follow)