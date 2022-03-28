from django.http import Http404
from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView

# from .models import User
from .models import Event

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

def all_events(request):
	event_list = Event.objects.all()
	return render(request, 'ymca/events_list.html',
	{'event_list':event_list})

def home(request):
	event_list = Event.objects.all()
	return render(request, 'ymca/home.html', {'event_list':event_list})

def create_event(request):
	return HttpResponse(request, 'http://127.0.0.1:8000/admin/ymca/event/add/')

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
