from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django import template
from django.contrib.auth.models import Group

# display messages
from django.contrib import messages

##from .models import User
from django.contrib.auth.models import User
from .models import Event
from .models import EventPackage
from .models import EventWeekDay

from .forms import EventForm
# https://alexpnt.github.io/2017/07/15/django-calendar/
# https://www.youtube.com/watch?v=Myrp1WqSwCk


# Create your views here.
# def index(request):
#     user_list = User.objects.order_by('username')[:5]
#     template = get_template('ymca/index.html')
#     context = {'user_list': user_list,}
#     return HttpResponse(template.render(context, request))

# def index(request):
#     # event_list = Event.objects.order_by('start_date')[:]
#     # template = get_template('ymca/YMCA-login.html')
#     # context = {'event_list': event_list,}
#     return render(request, 'ymca/YMCA-login.html')

def home(request):
	try:
		event_list = Event.objects.all()
	except:
		event_list = []

	return render(request, 'ymca/home.html', {'event_list':event_list})

def weekdays_to_string(weekdays_int_list):
	print("IN weekdays_to_string")
	print(weekdays_int_list)
	string_weekdays = ""
	for i in range(len(weekdays_int_list)):
		if(weekdays_int_list[i] == '1'):
			# string_weekdays_list.append("Monday")
			string_weekdays = string_weekdays + "Monday "
		elif(weekdays_int_list[i] == '2'):
			# string_weekdays_list.append("Tuesday")
			string_weekdays = string_weekdays + "Tuesday "
		elif(weekdays_int_list[i] == '3'):
			# string_weekdays_list.append("Wednesday")
			string_weekdays = string_weekdays + "Wednesday "
		elif(weekdays_int_list[i] == '4'):
			# string_weekdays_list.append("Thursday")
			string_weekdays = string_weekdays + "Thursday "
		elif(weekdays_int_list[i] == '5'):
			# string_weekdays_list.append("Friday")
			string_weekdays = string_weekdays + "Friday "
		elif(weekdays_int_list[i] == '6'):
			# string_weekdays_list.append("Saturday")
			string_weekdays = string_weekdays + "Saturday "
		else:
			# string_weekdays_list.append("Sunday")
			string_weekdays = string_weekdays + "Sunday "
	print(string_weekdays)
	# string_weekdays_list = listToString(string_weekdays_list)
	# print(string_weekdays_list)
	print("OUT weekdays_to_string")
	return string_weekdays


def searched(request):
	if request.method == 'GET':
		search = request.GET.get('search')
		test = User.objects.all().filter(username=search)
		if test.exists():
			userName = User.objects.get(username=search)
			eventIds = EventPackage.objects.all().filter(user_id=userName.id).values_list('event_id', flat=True)
			post = Event.objects.all().filter(id__in=eventIds)
			return render(request, 'ymca/home.html', {'event_list':post})
		else:
			post = Event.objects.all().filter(event_name='---------')
			return render(request, 'ymca/home.html', {'event_list':post})


def searched_user(request):
	if request.method == 'GET':
		search = request.GET.get('search')
		post = Event.objects.all().filter(event_name=search)
	return render(request, 'ymca/home.html', {'event_list':post})


def searched_users(request):
	if request.method == 'GET':
		search = request.GET.get('search')
		post = User.objects.all().filter(username=search)
	return render(request, 'ymca/view_users.html', {'user_list':post})

def all_events(request):
	event_list = Event.objects.all()
	return render(request, 'ymca/events_list.html',{'event_list':event_list})


def registered(request):
	if request.method == 'GET':
		test = User.objects.all().filter(username=request.user.username)
		if test.exists():
			userName = User.objects.get(username=request.user.username)
			eventIds = EventPackage.objects.all().filter(user_id=userName.id).values_list('event_id', flat=True)
			post = Event.objects.all().filter(id__in=eventIds)
			return render(request, 'ymca/home.html', {'event_list':post})
		else:
			post = Event.objects.all().filter(event_name='---------')
			return render(request, 'ymca/home.html', {'event_list':post})


def view_users(request):
	try:
		user_list = User.objects.all()
	except:
		user_list = []

	return render(request, 'ymca/view_users.html', {'user_list':user_list})


def deactivate(request, username):
	u = User.objects.all().get(id=username)
	if(u.is_active==True):
		eventIds = EventPackage.objects.all().filter(user_id=username).values_list('event_id', flat=True)
		event = Event.objects.all().filter(id__in=eventIds)
		for e in event:
			print("dec")
			e.taken_slots = e.taken_slots - 1
			e.save()
		eventPack = EventPackage.objects.all().filter(user_id=username)
		for e in eventPack:
			print("del")
			e.delete()
		u.is_active = False
		messages.info(request, 'USER DEACTIVATED')
	else:
		u.is_active = True
		messages.info(request, 'USER ACTIVATED')
	u.save()
	
	return view_users(request)

def delete(request, event_id):
	e = Event.objects.all().get(id=event_id)
	e.delete()

	return home(request)


def member(request, username):
	my_group = Group.objects.get(name='member') 
	user = User.objects.get(id=username)
	my_group.user_set.add(user)

	return view_users(request)

def nonmember(request, username):
	my_group = Group.objects.get(name='member') 
	user = User.objects.get(id=username)
	my_group.user_set.remove(user)

	return view_users(request)


def display_event_form(request):
	context = {}
	context['form'] = EventForm()
	return render(request, 'ymca/create-event.html', context)


def create_event(request):
	print("create_event")
	if(request.method == 'POST'):
		form = EventForm(request.POST)
		if(form.is_valid()):
			print(form.cleaned_data)
			data = {
				'event_name' : form.cleaned_data.get("event_name"),
				'start_date' : form.cleaned_data.get("start_date"),
				'end_date' : form.cleaned_data.get("end_date"),
				'start_time' : form.cleaned_data.get("start_time"),
				'end_time' : form.cleaned_data.get("end_time"),
				'slots' : form.cleaned_data.get("slots"),
				'taken_slots' : 0,
				'requirements' : form.cleaned_data.get("requirements"),
				'recurring' : form.cleaned_data.get("recurring"),
				'non_member_cost' : form.cleaned_data.get("non_member_cost"),
				'member_cost' : form.cleaned_data.get("member_cost"),
				'location' : form.cleaned_data.get("location"),
				'description' : form.cleaned_data.get("description")
			}
			print("/n")
			print(data)


			daysList = weekdays_to_string(data['recurring'])
			# Fix recurring later
			new_event = Event.objects.create(event_name = data['event_name'],
											 start_date = data['start_date'],
											 end_date = data['end_date'],
											 start_time = data['start_time'],
											 end_time = data['end_time'],
											 slots = data['slots'],
											 taken_slots = data['taken_slots'],
											 requirements = data['requirements'],
											 recurring = daysList,
											 non_member_cost = data['non_member_cost'],
											 member_cost = data['member_cost'],
											 location = data['location'],
											 description = data['description'])
			new_event.save()

			for day in data['recurring']:
				new_event_weekday = EventWeekDay.objects.create(event_id = new_event.id, weedday_id = int(day))
				new_event_weekday.save()
			return home(request) #ADD A SUCCESS URL
	return home(request)


def listToString(list):
	print("IN listToSting")
	str = ""
	for e in list:
		str = str + e
		str = str + " "
	print(str)
	print("OUT listToSting")
	return str

	# return HttpResponse(request, 'http://127.0.0.1:8000/admin/ymca/event/add/')
# def search_user_events(request, name):
# 	try:
# 		# user = User.objects.get(username == name)
# 		u_id = request.user.id
# 	except:
# 		print("No User Found")
# 		# Handle if user name was not found in the database
#
# 	user_events_list = Event.objects.all(id = EventPackage.objects.all(user_id == u_id).event_id)
#
# 	return render(request, 'ymca/events_list.html',{'event_list':user_events_list})


def register_for_event(request, event_id):
	print("IN register_for_event")
	username = request.user.username

	u_id = request.user.id
	event_object = Event.objects.get(id = event_id)
	action = "REGISTER"
	# is_conflic(u_id, event_object.id)
	if (event_object.taken_slots == event_object.slots):
		messages.info(request, 'ALL SLOTS ARE FULL. UNABLE TO SIGN UP')
		print("\nALL SLOTS ARE FULL. UNABLE TO SIGN UP")
		# return all_events(request)
	elif (is_signed_up(event_object.id, u_id)):
		messages.info(request, 'THE CURRENT USER IS ALREADY SIGNED UP FOR THIS CLASS')
		print("\nUSER WITH ID = " + str(u_id) + " ALREADY SIGNED UP FOR EVENT ID = " + str(event_object.id))
		# return all_events(request)
	elif (is_conflic(u_id, event_object.id)):
		messages.info(request, 'TIME CONFLICT WITH ALREADY EXISTING EVENT')
		print("\nTIME CONFLICT WITH ALREADY EXISTING EVENT")
	else:
		print("\nUPDATING SLOT COUNT FOR EVENT_ID = " + str(event_object.id) + " : " + str(event_object.taken_slots) + "/" + str(event_object.slots))
		event_object.taken_slots = event_object.taken_slots + 1
		event_object.save()
		print("\n***NEW SLOT COUNT FOR EVENT_ID = " + str(event_object.id) + " : " + str(event_object.taken_slots) + "/" + str(event_object.slots))
		print("\nREQUESTING UPDATE EVENT PACKAGE")
		update_event_packages(u_id, event_object.id, action)
		messages.info(request, 'SUCCESSFULLY ADDED CLASS')

	return home(request)


def drop_event(request, event_id):
	u_id = request.user.id
	event_object = Event.objects.get(id = event_id)
	action = "DROP"

	if(is_signed_up(event_object.id, u_id)):
		event_object.taken_slots = event_object.taken_slots - 1
		event_object.save()
		update_event_packages(u_id, event_object.id, action)
		messages.info(request, 'DROPPED EVENT')
	else:
		print("Unable to drop an event for which you did not register")
		messages.info(request, 'UNABLE TO DROP AN EVENT FOR WHICH YOU DID NOT REGISTER')

	return home(request)


# # # # ================== FIX ME ==================== # # # #
def is_conflic(u_id, e_id):
	event = Event.objects.get(id = e_id) #Get event for which to check conflict and trying to register
	days_of_event = list_day(event.id) #Get all days for this event. List of EventWeekDay objects
	# days_of_event = EventWeekDay.objects.filter(event_id = event.id)
	start_time_1 = event.start_time
	end_time_1 = event.end_time
	# print(event)
	# user_events = EventPackage.objects.filter(user_id = u_id) # QuerySet list
	# # print(user_events)
	# user_event_list = []
	#
	# # Convert QuerySet list to EventPackage list
	# for i in range(len(user_events)):
	# 	user_event_list.append(user_events[i])

	try:
		user_event_list = list_user_events(u_id) # get all user events. List of Events
		print(user_event_list)

		# e is Event object
		for e in user_event_list:
			print(e.id)
			# days_of_e_list is an int list
			days_of_e_list = list_day(e.id) # for each user event, get days for that event
			print(days_of_e_list)
			# days_of_e = EventWeekDay.objects.filter(event_id = e.id) # QuerySet list
			# print("========================+")
			# print(days_of_e)
			# print("========================+")
			# days_of_e_list = []
			#
			# # Convert QuerySet list to EventWeekDay list
			# for i in range(len(days_of_e)):
			# 	days_of_e_list.append(days_of_e[i])

			for i in range(len(days_of_event)):
				for j in range(len(days_of_e_list)):
					# print("========================")
					# print(day)
					# print(str(day.weedday_id))
					# print("========================")
					# print(days_of_e_list)
					# print("========================")
					if(days_of_event[i] == days_of_e_list[j]):
						start_time_2 = e.start_time
						end_time_2 = e.end_time
						print(str(start_time_1) + " - " + str(end_time_1))
						print('\n')
						print(str(start_time_2) + " - " + str(end_time_2))
						if((start_time_1 <= start_time_2 and start_time_2 <= end_time_1) or (start_time_1 <= end_time_2 and end_time_2 <= end_time_1)):
							print("returning a conflict in time")
							return True
	except:
		print("returning NO conflict in time")
		return False

def list_day(e_id):
	days_list = []
	# days_query_set = EventWeekDay.objects.filter(event_id = e_id)

	days_query_set = EventWeekDay.objects.all().filter(event_id = e_id)
	print("*** IN LIST DAYS")
	print(e_id)
	print(days_query_set)
	for d in range(len(days_query_set)):
		days_list.append(days_query_set[d].weedday_id)
	print(days_list)
	print("*** OUT LIST DAYS")
	return days_list

def list_user_events(u_id):
	print("*** IN LIST USER EVENTS")
	event_package_list = []
	event_query_set = EventPackage.objects.filter(user_id = u_id)
	print(event_query_set)

	for e in range(len(event_query_set)):
		event_package_list.append(event_query_set[e])
	print(event_package_list[0].event_id)

	user_event_list = []

	for e in event_package_list:
		print(e)
		event = Event.objects.get(id = e.event_id)
		user_event_list.append(event)
	print(user_event_list)
	print("*** OUT LIST USER EVENTS")
	return user_event_list


# event_1::  12:00  -  14:00
# event_2::       13:00  -  15:00
#
#

def is_signed_up(e_id, u_id):
	try:
		query_Event_package = EventPackage.objects.get(user_id = u_id, event_id = e_id)
		print("\nUSER_ID = " + str(u_id) + " ***IS*** SIGNED UP FOR EVENT_ID " + str(e_id))
		return True
	except:
		query_Event_package = None
		print("\nUSER_ID = " + str(u_id) + " ***IS NOT*** SIGNED UP FOR EVENT_ID " + str(e_id))
		return False


def update_event_packages(u_id, e_id, action):
	if(action == "REGISTER"):
		new_event_package = EventPackage.objects.create(user_id = u_id, event_id = e_id)
		new_event_package.save()
		print("\nSUCESSFULLY ADDED NEW EVENT PACKAGE FOR USER_ID = " + str(u_id) + " AND EVENT_ID = " + str(e_id))
	if(action == "DROP"):
		EventPackage.objects.filter(user_id = u_id, event_id = e_id).delete()


class SignUp(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"




# def login(request):
# 	if request.method == 'POST':
# 		if request.POST.get('username') and request.POST.get('password'):
# 				posted_username = request.POST.get('username')
# 				temp_username = User.objects.filter(username__startswith = posted_username)
#
# 				if temp_username is None:
# 					return render(request,'ymca/YMCA-login.html')
# 				else:
# 					posted_pwd = request.POST.get('password')
# 					temp_pwd = User.objects.filter(pwd__startswith = posted_pwd)
# 					if temp_pwd is None:
# 						return render(request,'ymca/YMCA-login.html')
# 					else:
# 						return render(request, 'ymca/YMCA-honeins.html')
# 		else:
# 			return render(request,'ymca/YMCA-login.html')

# def event_details(request, event_id):
#     try:
#         event = Event.objects.get(pk=event_id)
#     except Event.DoesNotExist:
#         raise Http404("Event does not exist")
#     return render(request, 'ymca/event_detail.html', {'event': event})
#
# def event(request, event_id):
#     return HttpResponse("You're looking at an event %s." % event_id)
#
# def description(request, event_id):
# 	response = "You are looking at the description of event %s"
# 	return HttpResponse(response % event_id)
#
# def sign_up(request, event_id):
#     return HttpResponse("You're signing for event %s." % event_id)
