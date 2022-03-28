from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
	path('signup/', views.SignUp.as_view(), name='signup'),
	path('events', views.all_events, name='list-events'),
	# path('YMCA-login/', views.login, name='login'),
	# path('<int:event_id>/', views.event_details, name='event_details'),
    # path('<int:event_id>/', views.event, name='event'),
    # path('<int:event_id>/description/', views.description, name='description'),
    # path('<int:event_id>/sign_up/', views.sign_up, name='sign_up'),
]
