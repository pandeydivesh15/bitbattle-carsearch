from django.contrib import admin

# Register your models here.
from .models import Dealer, MessageDealer

class DealerModelAdmin(admin.ModelAdmin):
	class Meta:
		model = Dealer
	list_display=["__unicode__"]

class MessageDealerModelAdmin(admin.ModelAdmin):
	class Meta:
		model = MessageDealer
	list_display=["__unicode__"]

admin.site.register(Dealer, DealerModelAdmin)
admin.site.register(MessageDealer, MessageDealerModelAdmin)