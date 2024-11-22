from django.contrib import admin
from .models import Profile, InventoryItem, Pattern, PatternImage
# Register your models here.
admin.site.register(Profile)
admin.site.register(InventoryItem)
admin.site.register(Pattern)
admin.site.register(PatternImage)

