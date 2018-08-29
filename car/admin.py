from django.contrib import admin

# Register your models here.
from .models import Car

class CarModelAdmin(admin.ModelAdmin):
	class Meta:
		model = Car
	list_display=["__unicode__"]

admin.site.register(Car, CarModelAdmin)