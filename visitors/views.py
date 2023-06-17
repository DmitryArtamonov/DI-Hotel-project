from django.shortcuts import render
from .models import RoomCategory, Room, Booking
from .forms import bookingForm

def homepage(request):
    context = {'categories': RoomCategory.objects.all}
    return render(request, 'homepage.html', context)


def booking(request):
    form = bookingForm()
    available = []

    if request.method == "POST":
        print(request.POST)

        # search form handling
        if 'find_button' in request.POST:
            form = bookingForm(request.POST)
            if form.is_valid():
                check_in = form.cleaned_data['check_in']
                check_out = form.cleaned_data['check_out']
                persons = form.cleaned_data['persons']
                booking_rooms = form.cleaned_data['rooms']

                # finding free rooms
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
                            'category':category,
                            'options': list(range(min(available_rooms, booking_rooms) + 1))
                        })

        # booking form handling
        elif 'booking_button' in request.POST:
            print('booking')

            categories = RoomCategory.objects.all()
            places = 0
            for category in categories:
                quantity = request.POST.get(f'quantity{category.id}')
                places += quantity * category.persons

            # check capacity:
            if places < persons:
                pass


            # Redirect or render a response
            # return redirect('booking_success')  # Example: redirect to a success page





    context = {
        'form': form,
        'available': available
        }
    return render(request, 'booking.html', context)





