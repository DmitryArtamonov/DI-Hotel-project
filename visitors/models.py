from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):

    # This fields save the data of the current booking to save it later and to use
    # as default in the form (not reset the form if user close it)
    current_booking_persons = models.IntegerField(default=2)
    current_booking_in = models.DateField(null=True, blank=True)
    current_booking_out = models.DateField(null=True, blank=True)


class RoomCategory(models.Model):
    title = models.CharField(max_length=50)
    persons = models.IntegerField()
    price = models.IntegerField()
    picture = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.title


class Room(models.Model):
    number = models.IntegerField(unique=True)
    category = models.ForeignKey(RoomCategory, on_delete=models.SET_NULL, blank=True, null=True, related_name='room')


    def __str__(self):
        return str(self.number)


class Visitor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Booking(models.Model):
    date_of_booking = models.DateTimeField(default=timezone.now)
    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    cost = models.IntegerField(null=True)
    rooms = models.ManyToManyField(Room)

    # def __str__(self):
    #     return self.id







