from django.shortcuts import render

from .models import Car
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count, Q

from user.models import check_if_auth_user, User

from dealer.models import MessageDealer

# Create your views here.
def car_detail(request, id):
	current_user = check_if_auth_user(request)
	if current_user:
		current_user = User.objects.get(email=current_user)
	else:
		messages.error(request, "Log in to view access this link.")
		return redirect("home")

	try:
		car_obj = Car.objects.get(pk=id)
	except Car.DoesNotExist: 
		messages.error(request, "Wrong link. Redirecting to home.")
		return redirect("home")


	email = request.POST.get('email')
	contact = request.POST.get('contact')
	message = request.POST.get('message')
	
	if email and contact and message:
		messages.success(request, "Query sent. Dealer will contact you soon.")
		message = MessageDealer(
			email=email,
			contact=int(contact),
			message=message,
			car_dealer=car_obj.car_dealer)
		message.save()

	# Get similar cars
	thres_price = 20000
	thres_year = 1
	same_dealer_cars = Car.objects.filter(
		year__range=(car_obj.year-thres_year, car_obj.year+thres_year),
		price__range=(car_obj.price-thres_price, car_obj.price+thres_price),
		car_dealer=car_obj.car_dealer).exclude(pk=car_obj.vin).order_by('-car_dealer__rating')
	
	diff_dealer_cars = Car.objects.filter(
		engine__startswith = str(car_obj.engine).split('.')[0],
		body__icontains = str(car_obj.body).split()[0],
		# transmission=car_obj.transmission,
		year__range=(car_obj.year-thres_year, car_obj.year+thres_year),
		price__range=(car_obj.price-thres_price, car_obj.price+thres_price)
		).exclude(car_dealer=car_obj.car_dealer).exclude(pk=car_obj.vin).order_by('-car_dealer__rating')

	same_make_model_cars = Car.objects.filter(
		make=car_obj.make,
		car_model=car_obj.car_model,
		engine=car_obj.engine,
		price__range=(car_obj.price-4*thres_price, car_obj.price+4*thres_price)).exclude(pk=car_obj.vin).order_by('-car_dealer__rating')

	# Same
	context_data = {
		'user': current_user,
		'obj': car_obj,
		'same_make_model_cars': same_make_model_cars[:20],
		'diff_dealer_cars': diff_dealer_cars[:20],
		'same_dealer_cars': same_dealer_cars[:20],
	}
	return render(request, "view_car.html" , context_data)


