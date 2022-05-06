from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
	path('signup/', views.SignUp.as_view(), name='signup'),
	# path('events', views.all_events, name='list-events'),
	path('register/<event_id>', views.register_for_event, name='register'),
	path('drop/<event_id>', views.drop_event, name='drop'),
	path('create-event/', views.create_event, name='create-event'),
	path('create-event-form', views.display_event_form, name='create-event-form'),
    path('searched', views.searched, name="searched"),
	path('searched-event', views.searched_user, name="searched-event"),
	path('registered', views.registered, name="registered"),
	path('view-users', views.view_users, name="view-users"),
	path('deactivate/<username>', views.deactivate, name="deactivate"),
	path('searched-users', views.searched_users, name="searched-users"),
	path('delete/<event_id>', views.delete, name="delete"),
	path('member/<username>', views.member, name="member"),
	path('nonmember/<username>', views.nonmember, name="nonmember"),
	# path('YMCA-login/', views.login, name='login'),
	# path('<int:event_id>/', views.event_details, name='event_details'),
    # path('<int:event_id>/', views.event, name='event'),
    # path('<int:event_id>/description/', views.description, name='description'),
    # path('<int:event_id>/sign_up/', views.sign_up, name='sign_up'),
]
