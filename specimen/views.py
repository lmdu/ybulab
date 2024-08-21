from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import *

# Create your views here.
def index(request):
	if request.user.is_authenticated:
		return render(request, 'index.html')
	
	return redirect('login')

def login(request):
	if request.user.is_authenticated:
		return redirect('index')
	elif request.method == 'GET':
		return render(request, 'login.html')
	elif request.method == 'POST':
		user_id = request.POST.get('userid')
		user_pwd = request.POST.get('userpass')

		print("user name: ", user_id, "user password: ", user_pwd)

def register(request):
	if request.user.is_authenticated:
		return redirect('index')
	elif request.method == 'GET':
		return render(request, 'register.html')
	elif request.method == 'POST':
		user = User.objects.create_user(
			username = request.POST.get('username'),
			password = request.POST.get('userpass'),
			email = request.POST.get('useremail')
		)
		user.profile.real = request.POST.get('userreal')
		user.save()

		return redirect('login')

def validate(request):
	if request.method == 'POST':
		if 'username' in request.POST:
			user_name = request.POST.get('username')
			query = User.objects.filter(username=user_name)
			return HttpResponse(str(not query.exists()).lower())

		elif 'useremail' in request.POST:
			user_email = request.POST.get('useremail')
			query = User.objects.filter(email=user_email)
			return HttpResponse(str(not query.exists()).lower())


def reset(request):
	pass
