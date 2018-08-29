from math import sin, cos, sqrt, atan2, radians
from geopy import distance, Point

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.db.models import Count, Q
from django.db import connection, transaction

from car.models import Car, load_all_makes, load_all_colors, load_all_trans
from dealer.models import Dealer

from user.models import User, check_if_auth_user, PastSearch

def show_index_page(request):
	all_makes = load_all_makes()
	all_colors = load_all_colors()
	all_transmissions = load_all_trans()

	cars_query_result = []
	current_user = check_if_auth_user(request)
	past_searches = []

	if current_user:
		current_user = User.objects.get(email=current_user)
		past_searches = PastSearch.objects.filter(
			search_user__auto_id=current_user.auto_id).order_by('-timestamp')

	location_name = request.POST.get('location_name')
	lat = request.POST.get('loc_latitude')
	lng = request.POST.get('loc_longitude')
	car_make = request.POST.get('car_make')
	max_distance = request.POST.get('max_distance')

	sort_by = request.POST.get('sort_by')
	max_price = request.POST.get('max_price')
	min_rating = request.POST.get('min_rating')
	car_color = request.POST.get('car_color')
	car_trans = request.POST.get('car_trans')

	if current_user and lat and lng and car_make:
		lat = float(lat)
		lng = float(lng)

		all_dealers = []
		all_dealers_query_set = Dealer.objects.all()

		if min_rating:
			all_dealers_query_set = all_dealers_query_set.filter(rating__gte=float(min_rating))

		if max_distance:
			max_distance = int(max_distance)
			for dlr in all_dealers_query_set:
				p1 = Point(str(lat) + " " + str(lng))
				p2 = Point(str(dlr.latitude) + " " + str(dlr.longitude))
				if max_distance >= distance.distance(p1,p2).kilometers:
					all_dealers.append(dlr)
		else:
			all_dealers = list(all_dealers_query_set)

		if not all_dealers:
				messages.error(request, "No cars exist for the given query. Try again.")

		if all_dealers:
			dealer_queries = [Q(car_dealer__uid=dlr.uid) for dlr in all_dealers]
			query = dealer_queries.pop()
			for q in dealer_queries:
				query |= q

			cars_query_result = Car.objects.filter(
				Q(make=car_make), query)

			if len(cars_query_result) == 0:
				messages.error(request, "No cars exist for the given query. Try again.")
			else:
				# Applying extra filters
				if max_price:
					cars_query_result = cars_query_result.filter(
						price__lte=int(max_price))

				if car_color and car_color != "No Choice":
					cars_query_result = cars_query_result.filter(
						color=str(car_color))

				if car_trans and car_trans != "No Choice":
					cars_query_result = cars_query_result.filter(
						transmission=car_trans)

				if sort_by:
					cars_query_result = cars_query_result.order_by(
						{'price': 'price', 'rating': '-car_dealer__rating'}[sort_by])

				if len(cars_query_result) == 0:
					messages.error(request, "No cars exist for the given query. Try again.")

			# Save this search if this is new.
			if len(cars_query_result) != 0:
				try:
					old_search = PastSearch.objects.get(
						location_name=location_name,
						location_lng=round(lng, 2),
						location_lat=round(lat, 2),
						car_make=car_make,
						max_distance=max_distance if max_distance else None,
						search_user=current_user)
					old_search.save()

				except PastSearch.DoesNotExist:
					new_search = PastSearch(
						location_name=location_name,
						location_lng=round(lng, 2),
						location_lat=round(lat, 2),
						car_make=car_make,
						max_distance=max_distance if max_distance else None,
						search_user=current_user)
					new_search.save()


	context_data = {
		"user" : current_user,
		"past_searches": past_searches,
		"all_makes": all_makes,
		"all_transmissions": all_transmissions,
		"all_colors": all_colors,
		"car_obj_list": cars_query_result,
		"search_query_lat": lat,
		"search_query_lng": lng,
		"search_query_name": location_name,
		"search_query_car_make": car_make,
		"search_query_max_dist": max_distance,
		"search_query_sort_by": sort_by,
		"search_query_max_price": max_price,
		"search_query_min_rating": min_rating,
		"search_query_car_color": car_color,
		"search_query_car_trans": car_trans,
	}
	return render(request, "index.html" , context_data)


def about_us(request):
	check = check_if_auth_user(request)
	
	context_data = {
		"user" : check,
	}
	return render(request, "aboutus.html" , context_data)