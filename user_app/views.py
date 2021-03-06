from django.shortcuts import render, HttpResponseRedirect, reverse
from .forms import CreateHeroForm, LoginHeroForm
from .models import HeroUser
from tasks.models import Task
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
import re

def loginUser(request):
  if request.method == "POST":
    form = LoginHeroForm(request.POST)
    if form.is_valid():
      data = form.cleaned_data
      if HeroUser.objects.filter(username=data['username']).exists():
        user = authenticate(username=data['username'], password=data['password'])
        login(request, user)
        return HttpResponseRedirect(request.GET.get('next', reverse('heroes')))
      else:
        return render(request, 'generic_form.html', {'form': form, 'title': 'Login Page', 'message': 'If you already have an account, please verify that you are using correct login credentials. If you do not have an account, please create one'})
  form = LoginHeroForm()
  return render(request, 'generic_form.html', {'form': form, 'title': "Login Page", 'message': 'Please Login into your account'})


def createUser(request):
  if request.method == 'POST':
    form = CreateHeroForm(request.POST)
    if form.is_valid():
      data = form.cleaned_data
      if HeroUser.objects.filter(username=data['username']).exists()==False:
        invalid_username = re.findall('\W', data['username'])
        if not invalid_username:
          if data['password'] == data['confirm_password']:
            new_user = HeroUser.objects.create_user(
            username=data['username'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            password=data['password'],
            interests = data['interests'], 
            website = data['website'],
            bio = data['bio'],
            age=data['age'],
            is_coach = data['is_coach']
            )
            if data['is_coach'] == True:
              new_user.is_staff = True
              new_user.save()
            Task.objects.create(
              task = "Navigate website, get to know who your fellow coaches/peers are, and start creating tasks",
              assigned_to = new_user
              )
            user = authenticate(username=data['username'], password=data['password'])
            login(request, user)
            return HttpResponseRedirect(reverse('heroes'))
          else:
            return render(request, 'generic_form.html', {'form': form, 'message': "Please make sure passwords match", 'title': "Create New Account"})
        else:
          return render(request, 'generic_form.html', {'form': form, 'title': 'Create New Account', 'message': 'Username invalid, please only use letters, numbers or _. Spaces and special characters are not allowed'})
      else:
        return render(request, 'generic_form.html', {'form': form, 'title': "Create New Account", 'message': 'Username is unavailable, please choose another.'})
  form = CreateHeroForm()
  return render(request, 'generic_form.html', {'form': form, 'title': "Create New Account", 'message': "Please fill out this form to create your new account"})


class LearnerDetailsView(LoginRequiredMixin, View):

    def get(self, request, user_id):
        learner = HeroUser.objects.get(id=user_id)
        assigned_tasks = Task.objects.filter(assigned_to=learner).order_by('completed')
        context = {
            'learner': learner,
            'assigned_tasks': assigned_tasks,
        }
        return render(request, 'learner_details.html', context)


class HeroesView(LoginRequiredMixin, View):

    def get(self, request):
        tasks = Task.objects.all().order_by('-completed')
        coaches = HeroUser.objects.filter(is_coach=True).order_by('interests')
        learners = HeroUser.objects.filter(is_coach=False).order_by('interests')
        context = {
            'coaches': coaches,
            'learners': learners,
            'tasks': tasks
        }
        return render(request, 'welcome.html', context)

def indexView(request):
    welcome = 'Welcome to iHero!'
    context = {
        'welcome': welcome,
    }
    return render(request, 'home.html', context)


class CoachDetailsView(LoginRequiredMixin, View):

    def get(self, request, user_id):
        coach = HeroUser.objects.get(id=user_id)
        assigned_tasks = Task.objects.filter(assigned_to=coach).order_by('completed')
        context = {
            'coach': coach,
            'assigned_tasks': assigned_tasks,
        }
        return render(request, 'coach_details.html', context)


@login_required
def coachList(request):
  tasks = Task.objects.filter(assigned_to__is_coach=True).order_by('-completed')
  coaches = HeroUser.objects.filter(is_coach=True).order_by('interests')
  return render(request, 'coaches.html', {'coaches': coaches, 'tasks': tasks})


@login_required
def learnerList(request):
  learners = HeroUser.objects.filter(is_coach=False).order_by('interests')
  tasks = Task.objects.filter(assigned_to__is_coach=False).order_by('-completed')
  return render(request, 'learners.html', {'learners': learners, 'tasks': tasks})


def logoutUser(request):
    logout(request)
    return HttpResponseRedirect(reverse("home"))


def handle404error(request, exception):
    return render(request, '404.html', status=404)


def handle500error(request):
    return render(request, '500.html', status=500)
