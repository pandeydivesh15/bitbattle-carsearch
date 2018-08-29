from django.db import models

# Create your models here.
class Dealer(models.Model):
	"""docstring for Farmer"""
	uid = models.IntegerField(primary_key=True)
	name = models.CharField(max_length=80)

	longitude = models.FloatField()
	latitude = models.FloatField()
	email = models.EmailField(max_length=80)
	rating = models.FloatField()
	num_ratings = models.IntegerField()
	
	def __unicode__(self):
		return self.name
	def __str__(self):
		return self.name

class MessageDealer(models.Model):
	auto_id = models.AutoField(primary_key=True)
	car_dealer = models.ForeignKey(Dealer, on_delete=models.CASCADE)
	message = models.CharField(max_length=300)
	email = models.CharField(max_length=50)
	contact = models.BigIntegerField()

	def __unicode__(self):
		return self.email + ": " + self.message[:10] + '...'
	def __str__(self):
		return self.email + ": " + self.message[:10] + '...'
