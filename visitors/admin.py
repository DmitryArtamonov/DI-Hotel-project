from django.contrib import admin

from .models import *

admin.site.register(User)
admin.site.register(RoomCategory)
admin.site.register(Room)
admin.site.register(Visitor)
admin.site.register(Booking)

