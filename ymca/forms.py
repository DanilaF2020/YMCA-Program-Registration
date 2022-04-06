from django import forms

class EventForm(forms.Form):
	event_name = forms.CharField(label='Event Name', max_length=100)
	start_date = forms.DateField()
	end_date = forms.DateField()
	start_time = forms.TimeField()
	end_time = forms.TimeField()
	slots = forms.IntegerField(label='Max Slots')
	requirements = forms.CharField(required=False, label='Requirements', max_length=200, initial="-")
	recurring = forms.MultipleChoiceField(required=True, initial=1, widget=forms.CheckboxSelectMultiple,
		choices=(
			(1, "Monday"),
			(2, "Tuesday"),
			(3, "Wednesday"),
			(4, "Thursday"),
			(5, "Friday"),
			(6, "Saturday"),
			(7, "Sunday")
		)
	)
	non_member_cost = forms.IntegerField()
	member_cost = forms.IntegerField()
	location = forms.CharField(max_length=200)
	description = forms.CharField(required=False, max_length=200, initial="-")
