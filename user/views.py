# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages

from django.db import connection, transaction

import datetime
import re

from passlib.hash import bcrypt

# Create your views here.
from .models import User, start_user_session, check_if_auth_user, stop_user_session, PastSearch

from portal.views import show_index_page

from collections import namedtuple

# Create your views here.
def check_login(request):
	if check_if_auth_user(request):
		messages.error(request, "Log out to perform Log in")
		return redirect("home")

	temp_id = request.POST.get("email")
	temp_pwd = request.POST.get("passwd")
	
	context_data = {}
	
	if temp_pwd and temp_id:
		try:
			person = User.objects.get(email=temp_id)
		except User.DoesNotExist:
			messages.error(request, "Enter correct user email")
			return redirect("home")

		if bcrypt.verify(temp_pwd, person.pwd):
			messages.success(request, "Successful Login")
			request = start_user_session(request, temp_id)
			return redirect("home")
		else:
			messages.error(request, "Please enter correct password")
			

	return redirect("home")


def signup_user(request):
	if check_if_auth_user(request):
		messages.error(request, "Log out to perform sign up")
		return redirect("home")

	name = request.POST.get('user_name')
	email = request.POST.get('user_email')
	pwd = request.POST.get('user_passwd')
	contact = request.POST.get('user_contact')
	
	if name and email and pwd and contact:
		flag = 0

		if len(pwd) < 6:
			flag = 1
			messages.error(request, "Make sure that password is minimum 6 characters long.")

		if not re.match("^[6789][0-9]{9}$", contact) or \
		   not re.match("^[a-z][_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$", email):
			flag = 1
			messages.error(request, "Make sure that:")
			messages.error(request, "1. Contact must be 10 digits long.")
			messages.error(request, "2. Also, make sure that that your mail ID is valid")

		if flag == 1:
			messages.error(request, "Please give proper credentials.")
			return redirect("user:signup")

		pwd = bcrypt.encrypt(pwd)

		new_user = User(name=name, email=email, pwd=pwd, contact=contact)

		try:
			new_user.save()
		except Exception:
			messages.error(request, "Entered mail ID is already registered.")
			return redirect("user:signup")
		
		messages.success(request, "Sign up was successful")
		messages.success(request, "Now you may login")

		return redirect("home")
	
	return render(request, "signup.html", {})

def logout_user(request):
	if stop_user_session(request):
		messages.success(request,"Logout Successful. Thank You for visiting")
		return redirect("home")
	else:
		messages.error(request,"Cant logout without any login")
		return redirect("home")

def show_past_search(request, _id):
	try:
		past_search = PastSearch.objects.get(pk=_id)
	except PastSearch.DoesNotExist:
		messages.error(request,"Wrong link. Redirecting to home.")
		return redirect("home")
	if check_if_auth_user(request) != past_search.search_user.email:
		messages.error(request,"You are not allowed to access this link. Redirecting to home.")
		return redirect("home")

	if not request.POST._mutable:
		request.POST._mutable = True

	request.POST["location_name"] = past_search.location_name
	request.POST['loc_latitude'] = past_search.location_lat
	request.POST['loc_longitude'] = past_search.location_lng
	request.POST['car_make'] = past_search.car_make
	request.POST['max_distance'] = past_search.max_distance

	request.POST._mutable = False

	return show_index_page(request)