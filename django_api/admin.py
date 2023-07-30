from django.contrib import admin
from .models import FoodItem, FoodType, Entity, Producer, Volunteer

# Register your models here.

admin.site.register(FoodItem)
admin.site.register(FoodType)
admin.site.register(Entity)
admin.site.register(Producer)
admin.site.register(Volunteer)