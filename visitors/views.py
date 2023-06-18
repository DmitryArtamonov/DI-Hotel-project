from datetime import timedelta

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView


from .models import RoomCategory, Room, Booking, User, Visitor
from .forms import bookingForm, SignupForm




def homepage(request):
    context = {'categories': RoomCategory.objects.all}
    return render(request, 'homepage.html', context)


def booking(request):
    form = bookingForm(user=request.user)
    available = []
    booking_request = ()
    if request.user.is_authenticated:
        error = ''
    else:
        error = 'Please login to make bookings'

    if request.method == "POST":

        # search form handling
        if 'find_button' in request.POST:
            form = bookingForm(request.POST)
            if form.is_valid():
                check_in = form.cleaned_data['check_in']
                check_out = form.cleaned_data['check_out']
                persons = form.cleaned_data['persons']

                cur_user = request.user
                cur_user.current_booking_persons = persons
                cur_user.current_booking_in = check_in
                cur_user.current_booking_out = check_out
                cur_user.save()

                # Saving request data. It should be attached to 'booking' button.
                # To get it with booking post request.
                # booking_request = (check_in.isoformat(), check_out.isoformat(), persons)

                # finding available rooms
                for category in RoomCategory.objects.all():
                    rooms = Room.objects.filter(category=category)
                    available_rooms = len(rooms)
                    for room in rooms:
                        if Booking.objects.filter(
                                rooms=room,
                                check_out__gt=check_in,
                                check_in__lt=check_out
                                ):
                            available_rooms -= 1
                    if available_rooms > 0:
                        available.append({
                            'category': category,
                            'options': list(range(available_rooms + 1)),
                            'places': available_rooms * category.persons
                        })

                # check enough places in available rooms
                available_places = 0
                for category in available:
                    available_places += category['places']
                if available_places < persons:
                    error = 'Sorry, there are no free rooms for your request'



        # booking form handling
        elif 'booking_button' in request.POST:
            # booking_data = request.POST['booking_button']
            categories = RoomCategory.objects.all()
            user = request.user
            persons = user.current_booking_persons
            check_in = user.current_booking_in
            check_out = user.current_booking_out

            # check capacity:
            places = 0
            for category in categories:
                quantity = request.POST.get(f'quantity{category.id}')
                if quantity:
                    quantity = int(quantity)
                else:
                    quantity = 0
                places += quantity * category.persons
            if places < int(persons):
                error = f'Not enough rooms to place {persons} persons. Add more rooms.'

            # create booking
            else:
                booking_data = []
                nights = (check_out - check_in).days
                booking = Booking(
                    visitor=Visitor.objects.get(user=user),
                    check_in=check_in,
                    check_out=check_out,
                )
                booking.save()
                for category in categories:
                    quantity = request.POST.get(f'quantity{category.id}')
                    if quantity:
                        for _ in range(int(quantity)):
                            for room in Room.objects.filter(category=category):
                                if Booking.objects.filter(
                                        rooms=room,
                                        check_out__gt=check_in,
                                        check_in__lt=check_out
                                ):
                                    continue

                                print('room', room)
                                booking.rooms.add(room)
                                break

                print('new booking:', booking.__dict__)
                booking.save()


                        # booking_data.append({'category': category,
                        #                      'rooms': quantity,
                        #                      'price': category.price * nights * quantity})

                return redirect('booking_approve')



    context = {
        'form': form,
        'available': available,
        'booking_request': booking_request,
        'error': error
    }
    print ('request', request)
    print('context', context)
    return render(request, 'booking.html', context)

def booking_approve(request, **kwargs):
    print (request)
    print(kwargs)



class SignupView(CreateView):
    form_class = SignupForm
    model = User
    template_name = "signup.html"
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        Visitor.objects.create(user=self.object)

        return response





