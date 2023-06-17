from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    pass


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
        return self.user.first_name+' '+self.user.last_name


class Booking(models.Model):
    date_of_booking = models.DateTimeField(default=timezone.now)
    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    cost = models.IntegerField()
    rooms = models.ManyToManyField(Room)

    def __str__(self):
        return self.id







