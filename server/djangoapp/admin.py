from django.contrib import admin
from .models import CarMake, CarModel


@admin.register(CarMake)
class CarMakeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "country")
    search_fields = ("name", "description", "country")
    ordering = ("name",)


@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "car_make", "dealer_id", "type", "year")
    list_filter = ("type", "year", "car_make")
    search_fields = ("name", "car_make__name")
    ordering = ("car_make__name", "name")