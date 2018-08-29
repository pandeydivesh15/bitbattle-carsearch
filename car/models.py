from django.db import models
from dealer.models import Dealer
from django.urls import reverse

ALL_MAKES = None
ALL_TRANS = None
ALL_COLORS = None

def load_all_makes():
	global ALL_MAKES
	if ALL_MAKES is not None:
		return ALL_MAKES
	
	ALL_MAKES = [x[0] for x in Car.objects.all().values_list('make').distinct()]
	return ALL_MAKES

def load_all_colors():
	global ALL_COLORS
	if ALL_COLORS is not None:
		return ALL_COLORS
	
	ALL_COLORS = [x[0] for x in Car.objects.all().values_list('color').distinct()]
	return ALL_COLORS

def load_all_trans():
	global ALL_TRANS
	if ALL_TRANS is not None:
		return ALL_TRANS
	
	ALL_TRANS = [x[0] for x in Car.objects.all().values_list('transmission').distinct()]
	return ALL_TRANS


# Create your models here.
class Car(models.Model):
	"""docstring for Farmer"""
	vin = models.CharField(max_length=80, primary_key=True)
	make = models.CharField(max_length=80)
	car_model = models.CharField(max_length=80)
	year = models.IntegerField()
	price = models.BigIntegerField()
	trim = models.CharField(max_length=80)
	engine = models.CharField(max_length=80)
	body = models.CharField(max_length=80)
	color = models.CharField(max_length=80)
	transmission = models.CharField(max_length=80)

	car_dealer = models.ForeignKey(Dealer, on_delete=models.CASCADE)
	
	def get_absolute_URL(self):
		return reverse("car:detail", kwargs={ "id":self.vin})

	def __unicode__(self):
		return self.trim 
	def __str__(self):
		return self.trim 
