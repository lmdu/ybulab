from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import *

# Create your views here.
def index(request):
	if request.user.is_authenticated:
		return render(request, 'index.html')
	else:
		return redirect('signin')

def signin(request):
	if request.user.is_authenticated:
		return redirect('index')
	elif request.method == 'GET':
		return render(request, 'signin.html')
	elif request.method == 'POST':
		user_id = request.POST.get('userid')
		user_pwd = request.POST.get('userpass')

		user = None
		if '@' in user_id:
			user = authenticate(email=user_id, password=user_pwd)

		if not user:
			user = authenticate(username=user_id, password=user_pwd)

		if user:
			login(request, user)
			return redirect('index')
		else:
			messages.error(request, "帐号或密码错误")
			return redirect('signin')

def signout(request):
	if request.user.is_authenticated:
		logout(request)
		return redirect('signin')

def signup(request):
	if request.user.is_authenticated:
		return redirect('index')
	elif request.method == 'GET':
		return render(request, 'signup.html')
	elif request.method == 'POST':
		user = User.objects.create_user(
			username = request.POST.get('username'),
			password = request.POST.get('userpass'),
			email = request.POST.get('useremail'),
			first_name = request.POST.get('userfirst'),
			last_name = request.POST.get('userlast')
		)
		#user.profile.real = request.POST.get('userreal')
		#user.save()

		return redirect('signin')

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

def species(request):
	term = request.GET.get('term')

	if not term:
		return JsonResponse({})

	rows = Species.objects.filter(Q(species_cn__icontains=term)|Q(species_en__icontains=term))[:50]
	items = [{'id': row.pk, 'text': "{} {}".format(row.species_en, row.species_cn)} for row in rows]
	return JsonResponse({
		'results': items,
		'pagination': {
			'more': False
		}
	})


def sample(request, action):
	if not request.user.is_authenticated:
		return redirect('login')

	if action == 'list':
		return render(request, 'sample-list.html')

	elif action == 'add':
		if request.method == 'GET':
			return render(request, 'sample-add.html')
		elif request.method == 'POST':
			pass

	elif action == 'edit':
		pass

	elif action == 'delete':
		pass




