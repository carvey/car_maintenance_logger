from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import View
from logger.models import Car, Entry
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic.edit import FormView
from django.contrib.auth.views import logout_then_login

class Login(FormView):
    template_name = 'login.html'
    form_class = AuthenticationForm
    success_url = '/'

    def form_valid(self, form):
        user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        login(self.request, user)
        if self.request.GET.get('next'):
            return HttpResponseRedirect(self.request.GET.get('next'))
        else:
            return super(Login, self).form_valid(form)


    # def get(self, request):
    #     form = AuthenticationForm()
    #     print request.GET.get('next')
    #     context = {
    #     'auth_form': form,
    #     'next': request.GET.get('next')
    #     }
    #     return render(request, self.template, context)

def logout(request):
    return logout_then_login(request, login_url='/login')

class Index(View):
    template = 'logger/index.html'

    @method_decorator(login_required())
    def get(self, request):

        cars = Car.objects.all()
        entries = Entry.objects.all()

        context = {
            'cars': cars,
            'entries': reversed(entries)
        }
        return render(request, self.template, context)


class CarProfile(View):
    template = 'logger/car_profile.html'

    @method_decorator(login_required())
    def get(self, request, car_id):
        car = Car.objects.get(id=car_id)
        entries = Entry.objects.filter(car=car)

        context = {
            'car': car,
            'entries': reversed(entries)
        }

        return render(request, self.template, context)


class EntryDetial(View):
    template = 'logger/entry_detail.html'

    @method_decorator(login_required())
    def get(self, request, entry_id):
        entry = Entry.objects.get(id=entry_id)

        context = {
            'entry': entry
        }

        return render(request, self.template, context)