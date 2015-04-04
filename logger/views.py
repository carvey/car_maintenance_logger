from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import View
from logger.models import Car, Entry
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormView
from django.contrib.auth.views import logout_then_login
from django.contrib.auth.models import User
from logger.forms import LoginForm, RegistrationForm, AddCarForm, AddEntryForm, EditCarForm, EditEntryForm
from django.template import RequestContext
from django.core.urlresolvers import reverse


class Login(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = '/'

    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        return self.render_to_response(self.get_context_data(form=form, next=self.request.GET.get('next')))

    def form_valid(self, form):
        user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        if not user:
            return HttpResponseRedirect('/login')
        login(self.request, user)
        if self.request.POST.get('next') != 'None':
            return HttpResponseRedirect(self.request.POST.get('next'))
        else:
            return super(Login, self).form_valid(form)


class Register(FormView):
    template_name = 'register.html'
    form_class = RegistrationForm
    success_url = '/login'

    def form_valid(self, form):
        username = form.cleaned_data['username']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']

        user = User.objects.create_user(username, email, password)
        user.save()
        return super(Register, self).form_valid(form)


def logout(request):
    return logout_then_login(request, login_url='/login')

class Index(View):
    template = 'logger/index.html'

    @method_decorator(login_required())
    def get(self, request):
        user = request.user
        cars = Car.objects.filter(user=user)
        entries = Entry.objects.filter(user=user)

        context = {
            'cars': cars,
            'entries': reversed(entries)
        }
        return render(request, self.template, context)


class CarProfile(View):
    template = 'logger/car_profile.html'

    @method_decorator(login_required())
    def get(self, request, car_id):
        user = request.user
        car = Car.objects.get(user=user, id=car_id)
        entries = Entry.objects.filter(user=user, car=car)

        context = {
            'car': car,
            'entries': reversed(entries)
        }

        return render(request, self.template, context)


def add_car(request):
    template = "logger/add_car.html"
    if request.method == "GET":
        form = AddCarForm()
    elif request.method == "POST":
        form = AddCarForm(request.POST)
        if form.is_valid():
            user = request.user
            label = form.cleaned_data['label']
            date_purchased = form.cleaned_data['date_purchased']
            initial_cost = form.cleaned_data['initial_cost']
            initial_mileage = form.cleaned_data['initial_mileage']

            car = Car(user=user, label=label,
                      date_purchased=date_purchased, initial_cost=initial_cost,
                      initial_mileage=initial_mileage)
            car.save()
            return HttpResponseRedirect(reverse("car_profile", args=[car.id]))
    context = {
        "form": form
    }
    return render(request, template, context)


class EntryDetial(View):
    template = 'logger/entry_detail.html'

    @method_decorator(login_required())
    def get(self, request, entry_id):
        user = request.user
        entry = Entry.objects.get(user=user, id=entry_id)

        context = {
            'entry': entry
        }

        return render(request, self.template, context)


def edit_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    car = entry.car

    if request.method == "GET":
        form = EditEntryForm(instance=entry)
        if form.is_valid():
            form.save()
    else:
        form = EditEntryForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()

        return HttpResponseRedirect('/cars/%s/' % car.id)

    context = {
        'entry': entry,
        'edit': True,
        'form': form
    }

    return render(request, 'logger/add_entry.html', context)


def edit_car(request, car_id):
    car = Car.objects.get(id=car_id)

    if request.method == "GET":
        form = EditCarForm(instance=car)
        if form.is_valid():
            form.save()
    else:
        form = EditCarForm(request.POST, instance=car)
        if form.is_valid():
            form.save()

            return HttpResponseRedirect('/cars/%s' % car.id)

    context = {
        'car': car,
        'edit': True,
        'form': form
    }

    return render(request, 'logger/add_car.html', context)


def add_entry(request, car_id):
    template = "logger/add_entry.html"

    user = request.user
    car = Car.objects.get(id=car_id, user=user)
    if request.method == "GET":
        form = AddEntryForm()
    elif request.method == "POST":
        form = AddEntryForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            mileage = form.cleaned_data['mileage']
            service_type = form.cleaned_data['service_type']
            service_location = form.cleaned_data['service_location']
            contact_name = form.cleaned_data['contact_name']
            contact_number = form.cleaned_data['contact_number']
            cost_of_parts = form.cleaned_data['cost_of_parts']
            cost_of_service = form.cleaned_data['cost_of_service']
            comments = form.cleaned_data['comments']

            entry = Entry(user=user, car=car, date=date, mileage=mileage, service_type=service_type,
                          service_location=service_location, contact_name=contact_name, contact_number=contact_number,
                          cost_of_parts=cost_of_parts, cost_of_service=cost_of_service, comments=comments)

            entry.save()

            car.mileage = mileage
            car.save()

            return HttpResponseRedirect(reverse("car_profile", args=[car.id]))
    context = {
        "form": form,
        "car": car,
    }
    return render(request, template, context)