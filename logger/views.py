from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import View
from logger.models import Car, Entry
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormView
from django.contrib.auth.views import logout_then_login
from django.contrib.auth.models import User
from logger.forms import LoginForm, RegistrationForm
from django.template import RequestContext


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