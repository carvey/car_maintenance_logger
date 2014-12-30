from django.shortcuts import render
from django.views.generic import View
from logger.models import Car, Entry

class Index(View):
    template = 'logger/index.html'

    def get(self, request):

        cars = Car.objects.all()
        entries = Entry.objects.all()

        context = {
            'cars': cars,
            'entries': entries
        }
        return render(request, self.template, context)

class CarProfile(View):
    template = 'logger/car_profile.html'

    def get(self, request, car_id):
        car = Car.objects.get(id=car_id)
        entries = Entry.objects.filter(car=car)

        context = {
            'car': car,
            'entries': entries
        }

        return render(request, self.template, context)


class EntryDetial(View):
    template = 'logger/entry_detail.html'

    def get(self, request, entry_id):
        entry = Entry.objects.get(id=entry_id)

        context = {
            'entry': entry
        }

        return render(request, self.template, context)