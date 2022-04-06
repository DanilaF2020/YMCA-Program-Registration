from django.db import models

# # Create your models here.
class User(models.Model):
	username = models.CharField(max_length=200)
	password = models.CharField(max_length=200)
	amount_due = models.IntegerField(default=0)
	membership_status = models.PositiveSmallIntegerField(
		choices=(
	        (1, "NonMember"),
	        (2, "Member"),
	    )
	)

	def __str__(self):
		return self.username

class Event(models.Model):
	event_name = models.CharField(max_length=200)
	start_date = models.DateField('start date')
	end_date = models.DateField('end date')
	start_time = models.TimeField('start time')
	end_time = models.TimeField('end time')
	slots = models.IntegerField(default=0)
	taken_slots = models.IntegerField(default=0)
	requirements = models.CharField(max_length=200, default='None')
	# recurring = models.DateField(u'Day of the event', help_text=u'Day of the event')
	recurring = models.PositiveSmallIntegerField(
		choices=(
			(1, "Daily"),
			(2, "Every Other Day"),
			(3, "Weekly"),
			(4, "Never"),
			(5, "Other..."),
		)
	)
	non_member_cost = models.IntegerField(default=0)
	member_cost = models.IntegerField(default=0)
	location = models.CharField(max_length=200)
	description = models.CharField(max_length=200, default='')

	def __str__(self):
		return self.event_name

class EventPackage(models.Model):
	user_id = models.IntegerField(default=0)
	event_id = models.IntegerField(default=0)

# class Role(models.Model):
# 	role_name = models.PositiveSmallIntegerField(
# 		choices=(
# 	        (1, "NonMember"),
# 	        (2, "Member"),
# 	    )
# 	)
