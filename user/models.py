from django.db import models
from django.urls import reverse

# Create your models here.
class User(models.Model):
	"""docstring for Farmer"""
	auto_id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=30)

	email = models.EmailField(max_length=30,unique=True)
	pwd = models.CharField(max_length=100)

	contact = models.BigIntegerField()

	join_timestamp = models.DateTimeField(auto_now=False,auto_now_add=True)
	
	def __unicode__(self):
		return self.name
	def __str__(self):
		return self.name

class PastSearch(models.Model):
	auto_id = models.AutoField(primary_key=True)
	location_name = models.CharField(max_length=100)
	location_lng = models.FloatField()
	location_lat = models.FloatField()

	car_make = models.CharField(max_length=30)
	max_distance = models.IntegerField(null=True)

	search_user = models.ForeignKey(User, on_delete=models.CASCADE)

	timestamp = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return self.name
	def __str__(self):
		return self.name

	def get_absolute_URL(self):
		return reverse("user:search", kwargs={ "_id":self.auto_id})


def start_user_session(request, user_id):
	request.session["user_mail_id"] = user_id
	return request

def check_if_auth_user(request):
	if request.session.has_key("user_mail_id"):
		return request.session["user_mail_id"]
	else:
		return None

def stop_user_session(request):
	if request.session.has_key("user_mail_id"):
		del request.session["user_mail_id"]
		return True
	return False