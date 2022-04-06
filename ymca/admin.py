from django.contrib import admin

from .models import Event
from .models import User
from .models import EventPackage
from .models import EventWeekDay


# from .models import Role
# Register your models here.
admin.site.register(Event)
admin.site.register(User)
admin.site.register(EventPackage)
admin.site.register(EventWeekDay)
# admin.site.register(Role)
