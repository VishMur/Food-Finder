from django.contrib import admin
from .models import FoodItem, FoodType, Entity, Producer, Volunteer, ProducerBookmark

# Register your models here.

models_to_register = [
    FoodItem,
    FoodType,
    Entity,
    Producer,
    Volunteer,
    ProducerBookmark,

]

for model in models_to_register:
    admin.site.register(model)