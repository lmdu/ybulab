from django.urls import reverse
from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .forms import *
from .models import *

# Create your views here.
def index(request):
	if request.user.is_authenticated:
		photos = Resource.objects.filter(uptype=1).order_by('-uptime')[0:10]
		counts = {}
		counts['sample'] = Sample.objects.count()
		counts['specimen'] = Specimen.objects.count()
		counts['user'] = User.objects.count()
		counts['species'] = Species.objects.count() 

		return render(request, 'index.html', {
			'photos': photos,
			'counts': counts,
		})
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
			if user.profile.identity == 0:
				messages.error(request, "你的帐号未激活, 请联系管理员审核")
				return render(request, 'error.html')

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

		return redirect('signin')

def validate(request):
	if request.method == 'POST':
		if 'username' in request.POST:
			user_name = request.POST.get('username')
			query = User.objects.filter(username=user_name)

		elif 'useremail' in request.POST:
			user_email = request.POST.get('useremail')
			query = User.objects.filter(email=user_email)

		elif 'sampleid' in request.POST:
			sample_id = request.POST.get('sampleid')
			query = Sample.objects.filter(sample_code=sample_id)

		elif 'specimenid' in request.POST:
			specimen_id = request.POST.get('specimenid')
			query = Specimen.objects.filter(specimen_code=specimen_id)

		elif 'speciesid' in request.POST:
			species_id = request.POST.get('speciesid')
			query = Species.objects.filter(species_en=species_id)

		return HttpResponse(str(not query.exists()).lower())

def setpass(request, action):
	if not request.user.is_authenticated:
		return redirect('signin')

	if action == 'view':
		if request.method == 'GET':
			return render(request, 'setpass.html')

	elif action == 'edit':
		if request.method == 'POST':
			uid = int(request.POST.get('uid'))
			old = request.POST.get('old_passwd')
			new = request.POST.get('new_passwd')
			user = User.objects.get(pk=uid)

			if user.check_password(old):
				user.set_password(new)
				user.save()
				logout(request)
				return redirect('signin')
			else:
				messages.error(request, "输入的原始密码错误!")
				return render(request, 'error.html')

def species(request, action):
	if not request.user.is_authenticated:
		return redirect('signin')

	if action == 'select':
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

	elif action == 'list':
		if request.method == 'GET':
			return render(request, "species-list.html")

		elif request.method == 'POST':
			draw = int(request.POST.get('draw'))
			start = int(request.POST.get('start', 0))
			length = int(request.POST.get('length', 10))

			if length == -1:
				length = 10

			term = request.POST.get('search[value]', '').strip()
			speciess = Species.objects.all()
			total_count = speciess.count()
			filter_count = total_count

			if term:
				speciess = speciess.filter(
					Q(species_en__icontains = term) |
					Q(species_cn__icontains = term) |
					Q(kingdom_en__icontains = term) |
					Q(kingdom_cn__icontains = term) |
					Q(phylum_en__icontains = term) |
					Q(phylum_cn__icontains = term) |
					Q(class_en__icontains = term) |
					Q(class_cn__icontains = term) |
					Q(order_en__icontains = term) |
					Q(order_cn__icontains = term) |
					Q(family_en__icontains = term) |
					Q(family_cn__icontains = term) |
					Q(genus_en__icontains = term) |
					Q(genus_cn__icontains = term)
				)
				filter_count = speciess.count()

			rows = []
			for s in speciess[start:start+length]:
				buttons = []

				if request.user.profile.identity > 2:
					buttons.append('<a href="{}?sid={}" class="ms-2 btn btn-sm btn-outline-secondary">编辑</a>'.format(
						reverse('species', kwargs={'action': 'edit'}),
						s.id
					))

					buttons.append('<button data-target="{}" class="ms-2 btn btn-sm btn-outline-danger delete-species" data-bs-toggle="modal" data-bs-target="#delete-species-dialog">删除</button>'.format(
						s.id
					))

				rows.append([
					s.id,
					"{}<br>{}".format(s.kingdom_cn, s.kingdom_en),
					"{}<br>{}".format(s.phylum_cn, s.phylum_en),
					"{}<br>{}".format(s.class_cn, s.class_en),
					"{}<br>{}".format(s.order_cn, s.order_en),
					"{}<br>{}".format(s.family_cn, s.family_en),
					"{}<br>{}".format(s.genus_cn, s.genus_en),
					"{}<br><i>{}</i>".format(s.species_cn, s.species_en),
					''.join(buttons)
				])

			return JsonResponse({
				'draw': draw,
				'recordsTotal': total_count,
				'recordsFiltered': filter_count,
				'data': rows
			})

	elif action == 'add':
		if user.profile.identity < 2:
			messages.error(request, "你没有添加物种的权限, 请联系管理员")
			return render(request, 'error.html')

		if request.method == 'GET':
			return render(request, "species-add.html")

		elif request.method == 'POST':
			form = SpeciesForm(request.POST)

			if form.is_valid():
				form.save()
				return redirect(reverse('species', kwargs={'action': 'list'}))

	elif action == 'edit':
		if user.profile.identity < 2:
			messages.error(request, "你没有编辑物种的权限, 请联系管理员")
			return render(request, 'error.html')

		if request.method == 'GET':
			sid = int(request.GET.get('sid', 0))
			species = Species.objects.get(id=sid)
			return render(request, "species-edit.html", {
				'species': species
			})

		elif request.method == 'POST':
			sid = int(request.POST.get('sid', 0))
			species = Species.objects.get(id=sid)

			form = SpeciesForm(instance=species, data=request.POST)

			if form.is_valid():
				form.save()
				return redirect(reverse('species', kwargs={'action': 'list'}))

	elif action == 'delete':
		if user.profile.identity < 2:
			messages.error(request, "你没有删除物种的权限, 请联系管理员")
			return render(request, 'error.html')

		if request.method == 'POST':
			sid = int(request.POST.get('sid', 0))
			species = Species.objects.get(id=sid)
			species.delete()

			return redirect(reverse('species', kwargs={'action': 'list'}))

def customer(request, action):
	if not request.user.is_authenticated:
		return redirect('signin')

	if request.user.profile.identity < 4:
		messages.error(request, "你没有管理用户的权限, 请联系管理员")
		return render(request, 'error.html')

	if action == 'list':
		if request.method == 'GET':
			return render(request, "customer-list.html")

		elif request.method == 'POST':
			draw = int(request.POST.get('draw'))
			start = int(request.POST.get('start', 0))
			length = int(request.POST.get('length', 10))

			if length == -1:
				length = 10

			term = request.POST.get('search[value]', '').strip()
			users = User.objects.all()
			total_count = users.count()
			filter_count = total_count

			if term:
				users = users.filter(
					Q(username__icontains = term) |
					Q(email__icontains = term) |
					Q(last_name__icontains = term) |
					Q(first_name__icontains = term) |
					Q(profile__phone__icontains = term) |
					Q(profile__major__icontains = term) |
					Q(profile__resume__icontains = term)
				)
				filter_count = users.count()

			rows = []
			for user in users[start:start+length]:
				buttons = []

				if request.user.profile.identity > 2:
					buttons.append('<a href="{}?uid={}" class="ms-2 btn btn-sm btn-outline-secondary">编辑</a>'.format(
						reverse('customer', kwargs={'action': 'edit'}),
						user.id
					))

					if user.profile.identity < 4:
						buttons.append('<button data-target="{}" class="ms-2 btn btn-sm btn-outline-danger delete-user" data-bs-toggle="modal" data-bs-target="#delete-user-dialog">删除</button>'.format(
							user.id
						))

				rows.append([
					user.id,
					user.username,
					user.email,
					"{}{}".format(user.last_name, user.first_name),
					user.profile.phone,
					user.profile.get_title_display(),
					user.profile.get_degree_display(),
					user.profile.get_position_display(),
					user.profile.major,
					user.profile.get_status_display(),
					user.profile.get_identity_display(),
					''.join(buttons)
				])

			return JsonResponse({
				'draw': draw,
				'recordsTotal': total_count,
				'recordsFiltered': filter_count,
				'data': rows
			})

	elif action == 'add':
		if request.method == 'GET':
			return render(request, "customer-add.html")

		elif request.method == 'POST':
			form = CustomerForm(request.POST)

			if form.is_valid():
				form.save()
				return redirect(reverse('customer', kwargs={'action': 'list'}))

	elif action == 'edit':
		if request.method == 'GET':
			uid = int(request.GET.get('uid', 0))
			customer = User.objects.get(id=uid)
			return render(request, "customer-edit.html", {
				'customer': customer
			})

		elif request.method == 'POST':
			uid = int(request.POST.get('uid', 0))
			user = User.objects.get(id=uid)

			user_form = UserForm(instance=user, data=request.POST)
			profile_form = ProfileForm(instance=user.profile, data=request.POST)

			if user_form.is_valid() and profile_form.is_valid():
				profile = profile_form.save()
				customer = user_form.save(commit=False)
				customer.profile = profile
				customer.save()
				return redirect(reverse('customer', kwargs={'action': 'list'}))

	elif action == 'delete':
		if request.method == 'POST':
			uid = int(request.POST.get('uid', 0))
			user = User.objects.get(id=uid)
			user.delete()

			return redirect(reverse('customer', kwargs={'action': 'list'}))

@login_required
def upload(request):
	if request.method == 'POST':
		upfile = request.FILES.get('file')
		uptype = 0
		if upfile.content_type.startswith('image'):
			uptype = 1

		r = Resource.objects.create(
			upfile = upfile,
			uptype = uptype
		)

		return JsonResponse({'id': r.pk, 'type': 'photos' if uptype else 'attachments'})

def sample(request, action):
	if not request.user.is_authenticated:
		return redirect('signin')

	if action == 'list':
		if request.method == 'GET':
			return render(request, 'sample-list.html')

		elif request.method == 'POST':
			draw = int(request.POST.get('draw'))
			start = int(request.POST.get('start', 0))
			length = int(request.POST.get('length', 10))

			if length == -1:
				length = 10

			term = request.POST.get('search[value]', '').strip()
			samples = Sample.objects.all()
			total_count = samples.count()
			filter_count = total_count

			if term:
				samples = samples.filter(
					Q(sample_code__icontains = term) |
					Q(sample_name__icontains = term) |
					Q(sample_tissue__icontains = term) |
					Q(collect_location__icontains = term) |
					Q(collect_people__icontains = term) |
					Q(store_place__icontains = term) |
					Q(species__species_en__icontains = term) |
					Q(species__species_cn__icontains = term)
				)
				filter_count = samples.count()

			rows = []
			for s in samples[start:start+length]:
				buttons = ['<a href="{}?sid={}" class="btn btn-sm btn-outline-primary">详情</a>'.format(
					reverse('sample', kwargs={'action': 'view'}),
					s.id
				)]

				if request.user.profile.identity > 2:
					buttons.append('<a href="{}?sid={}" class="ms-2 btn btn-sm btn-outline-secondary">编辑</a>'.format(
						reverse('sample', kwargs={'action': 'edit'}),
						s.id
					))

					buttons.append('<button data-target="{}" class="ms-2 btn btn-sm btn-outline-danger delete-sample" data-bs-toggle="modal" data-bs-target="#delete-sample-dialog">删除</button>'.format(
						s.id
					))

				rows.append([
					s.id,
					s.sample_code,
					s.sample_name,
					s.sample_tissue,
					s.species.species_en,
					s.species.species_cn,
					s.collect_location,
					s.store_place,
					''.join(buttons)
				])

			return JsonResponse({
				'draw': draw,
				'recordsTotal': total_count,
				'recordsFiltered': filter_count,
				'data': rows
			})

	elif action == 'add':
		if request.user.profile.identity < 2:
			messages.error(request, "你没有添加样本的权限, 请联系管理员")
			return render(request, 'error.html')

		if request.method == 'GET':
			return render(request, 'sample-add.html')

		elif request.method == 'POST':
			form = SampleForm(request.POST)

			if form.is_valid():
				s = form.save(commit=False)
				s.creator = request.user
				s.save()

				return redirect(reverse('sample', kwargs={'action': 'list'}))

			print(form.errors)

	elif action == 'edit':
		if request.user.profile.identity < 2:
			messages.error(request, "你没有添加样本的权限, 请联系管理员")
			return render(request, 'error.html')

		if request.method == 'GET':
			sid = int(request.GET.get('sid', 0))
			sample = Sample.objects.get(pk=sid)

			if request.user.profile.identity == 2:
				if request.user.id != sample.creator.id:
					messages.error(request, "你没有修改样本信息的权限, 请联系管理员")
					return render(request, 'error.html')

			pids = [int(i) for i in sample.photos]
			aids = [int(j) for j in sample.attachments]
			photos = Resource.objects.filter(pk__in=pids)
			attachments = Resource.objects.filter(pk__in=aids)

			return render(request, 'sample-edit.html', {
				'sample': sample,
				'photos': photos,
				'attachments': attachments,
			})

		elif request.method == 'POST':
			sid = int(request.POST.get('sid', 0))
			sample = Sample.objects.get(pk=sid)

			if request.user.profile.identity == 2:
				if request.user.id != sample.creator.id:
					messages.error(request, "你没有修改样本信息的权限, 请联系管理员")
					return render(request, 'error.html')

			form = SampleForm(instance=sample, data=request.POST)

			if form.is_valid():
				form.save()
				return redirect(reverse('sample', kwargs={'action': 'list'}))

	elif action == 'delete':
		if request.user.profile.identity < 2:
			messages.error(request, "你没有删除样本的权限, 请联系管理员")
			return render(request, 'error.html')

		if request.method == 'POST':
			sid = int(request.POST.get('sid', 0))
			sample = Sample.objects.get(pk=sid)

			if request.user.profile.identity == 2:
				if request.user.id != sample.creator.id:
					messages.error(request, "你没有删除样本的权限, 请联系管理员")
					return render(request, 'error.html')

			pids = [int(i) for i in sample.photos]
			aids = [int(j) for j in sample.attachments]
			Resource.objects.filter(pk__in=pids).delete()
			Resource.objects.filter(pk__in=aids).delete()
			sample.delete()

			return redirect(reverse('sample', kwargs={'action': 'list'}))

	elif action == 'view':
		if request.method == 'GET':
			sid = int(request.GET.get('sid', 0))
			sample = Sample.objects.get(pk=sid)
			pids = [int(i) for i in sample.photos]
			aids = [int(j) for j in sample.attachments]
			photos = Resource.objects.filter(pk__in=pids)
			attachments = Resource.objects.filter(pk__in=aids)

			return render(request, 'sample-view.html', {
				'sample': sample,
				'photos': photos,
				'attachments': attachments
			})

def specimen(request, action):
	if not request.user.is_authenticated:
		return redirect('signin')

	if action == 'list':
		if request.method == 'GET':
			return render(request, 'specimen-list.html')

		elif request.method == 'POST':
			draw = int(request.POST.get('draw'))
			start = int(request.POST.get('start', 0))
			length = int(request.POST.get('length', 10))

			if length == -1:
				length = 10

			term = request.POST.get('search[value]', '').strip()
			specimens = Specimen.objects.all()
			total_count = specimens.count()
			filter_count = total_count

			if term:
				specimens = specimens.filter(
					Q(specimen_code__icontains = term) |
					Q(specimen_name__icontains = term) |
					Q(collect_location__icontains = term) |
					Q(collect_people__icontains = term) |
					Q(store_place__icontains = term) |
					Q(species__species_en__icontains = term) |
					Q(species__species_cn__icontains = term)
				)
				filter_count = specimens.count()

			rows = []
			for s in specimens[start:start+length]:
				buttons = ['<a href="{}?sid={}" class="btn btn-sm btn-outline-primary">详情</a>'.format(
					reverse('specimen', kwargs={'action': 'view'}),
					s.id
				)]

				if request.user.profile.identity > 2:
					buttons.append('<a href="{}?sid={}" class="ms-2 btn btn-sm btn-outline-secondary">编辑</a>'.format(
						reverse('specimen', kwargs={'action': 'edit'}),
						s.id
					))

					buttons.append('<button data-target="{}" class="ms-2 btn btn-sm btn-outline-danger delete-specimen" data-bs-toggle="modal" data-bs-target="#delete-specimen-dialog">删除</button>'.format(
						s.id
					))

				rows.append([
					s.id,
					s.specimen_code,
					s.specimen_name,
					s.get_specimen_gender_display(),
					s.species.species_en,
					s.species.species_cn,
					s.collect_location,
					s.store_place,
					''.join(buttons)
				])

			return JsonResponse({
				'draw': draw,
				'recordsTotal': total_count,
				'recordsFiltered': filter_count,
				'data': rows
			})

	elif action == 'add':
		if request.user.profile.identity < 2:
			messages.error(request, "你没有添加标本的权限, 请联系管理员")
			return render(request, 'error.html')

		if request.method == 'GET':
			return render(request, 'specimen-add.html')

		elif request.method == 'POST':
			form = SpecimenForm(request.POST)

			if form.is_valid():
				s = form.save(commit=False)
				s.creator = request.user
				s.save()

				return redirect(reverse('specimen', kwargs={'action': 'list'}))

	elif action == 'edit':
		if request.user.profile.identity < 2:
			messages.error(request, "你没有添加标本的权限, 请联系管理员")
			return render(request, 'error.html')

		if request.method == 'GET':
			sid = int(request.GET.get('sid', 0))
			specimen = Specimen.objects.get(pk=sid)

			if request.user.profile.identity == 2:
				if request.user.id != specimen.creator.id:
					messages.error(request, "你没有修改样本信息的权限, 请联系管理员")
					return render(request, 'error.html')

			pids = [int(i) for i in specimen.photos]
			aids = [int(j) for j in specimen.attachments]
			photos = Resource.objects.filter(pk__in=pids)
			attachments = Resource.objects.filter(pk__in=aids)

			return render(request, 'specimen-edit.html', {
				'specimen': specimen,
				'photos': photos,
				'attachments': attachments,
			})

		elif request.method == 'POST':
			sid = int(request.POST.get('sid', 0))
			specimen = Specimen.objects.get(pk=sid)

			if request.user.profile.identity == 2:
				if request.user.id != specimen.creator.id:
					messages.error(request, "你没有修改标本信息的权限, 请联系管理员")
					return render(request, 'error.html')

			form = SpecimenForm(instance=specimen, data=request.POST)

			if form.is_valid():
				form.save()
				return redirect(reverse('specimen', kwargs={'action': 'list'}))

	elif action == 'delete':
		if request.user.profile.identity < 2:
			messages.error(request, "你没有删除标本的权限, 请联系管理员")
			return render(request, 'error.html')

		if request.method == 'POST':
			sid = int(request.POST.get('sid', 0))
			specimen = Specimen.objects.get(pk=sid)

			if request.user.profile.identity == 2:
				if request.user.id != specimen.creator.id:
					messages.error(request, "你没有删除样本的权限, 请联系管理员")
					return render(request, 'error.html')

			pids = [int(i) for i in specimen.photos]
			aids = [int(j) for j in specimen.attachments]
			Resource.objects.filter(pk__in=pids).delete()
			Resource.objects.filter(pk__in=aids).delete()
			specimen.delete()

			return redirect(reverse('specimen', kwargs={'action': 'list'}))

	elif action == 'view':
		if request.method == 'GET':
			sid = int(request.GET.get('sid', 0))
			specimen = Specimen.objects.get(pk=sid)
			pids = [int(i) for i in specimen.photos]
			aids = [int(j) for j in specimen.attachments]
			photos = Resource.objects.filter(pk__in=pids)
			attachments = Resource.objects.filter(pk__in=aids)

			return render(request, 'specimen-view.html', {
				'specimen': specimen,
				'photos': photos,
				'attachments': attachments
			})

def profile(request, action):
	if not request.user.is_authenticated:
		return redirect('signin')

	if action == 'view':
		if request.method == 'GET':
			return render(request, 'profile.html')

	elif action == 'edit':
		if request.method == 'POST':
			uid = int(request.POST.get('uid', 0))
			user = User.objects.get(id=uid)

			user_form = UserForm(instance=user, data=request.POST)
			profile_form = ProfileForm(instance=user.profile, data=request.POST)

			if user_form.is_valid() and profile_form.is_valid():
				profile = profile_form.save()
				customer = user_form.save(commit=False)
				customer.profile = profile
				customer.save()
				return redirect(reverse('profile', kwargs={'action': 'view'}))

