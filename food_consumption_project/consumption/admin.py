from django.contrib import admin
from .models import FoodType, Consumer, Consumption

# Register your models here.

admin.site.register(FoodType)
admin.site.register(Consumer)
admin.site.register(Consumption)
