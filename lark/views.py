from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from lark.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.http import (
		HttpResponseRedirect, HttpResponse, Http404, 
		JsonResponse
		)
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.template import RequestContext

from datetime import datetime
from time import strftime

from rest_framework.renderers import JSONRenderer
from lark.models import (
		Task, 
		TestCase, 
		UserProfile, 
		Submission_judge,
		Submission,
		Submission_test
		)
from lark.forms import CodeForm
from lark.serializers import (
		TaskSerializer,
		SubmissionSerializer,
		Submission_testSerializer
		)

@login_required
def index(request):
	task_list = Task.objects.all().order_by('name')
	context_dict = {'tasks': task_list}
	return render(request, 'lark/index.html', context_dict)

def get_task_list(max_result=0, starts_with=''):
	task_list = []
	if starts_with:
		task_list = Task.objects.filter(name__startswith=starts_with).order_by('name')
	else:
		task_list = Task.objects.all().order_by('name')

	return task_list

def search_task(request):
	task_list = []
	starts_with = ''
	if request.method == 'GET':
		starts_with = request.GET['search']

	task_list = get_task_list(10, starts_with)

	data = [TaskSerializer(task).data for task in task_list]
	return JsonResponse({"tasks": data})

def list_submissions(request):
	user = request.GET['user']
	task_url = request.GET['task']
	task = get_object_or_404(Task, url=task_url)
	user = get_object_or_404(UserProfile, id=request.user.id)
	sub_list = Submission.objects.filter(user=user, task=task).order_by('-date')[:5]
	data = [SubmissionSerializer(sub).data for sub in sub_list]
	for sub in data:
		sub['date'] = strftime('%Y-%m-%d %H:%M');
	return JsonResponse({"subs": data})

@login_required
def detail(request, task_url):
	form = CodeForm()
	task = get_object_or_404(Task, url=task_url)
	user = get_object_or_404(UserProfile, id=request.user.id)
	subs = Submission.objects.filter(user=user, task=task).order_by('-date')[:5]
	print subs
	upload_error = request.session.pop('error_message', None)
	context_dict = {
		'user': user,
		'task': task,
		'form': form,
		'subs': subs,
		'error_message': upload_error
	}
	return render(request, 'lark/detail.html', context_dict)

@login_required
def submit(request, task_url):
	form = CodeForm(request.POST, request.FILES)
	context_dict = {}
	if form.is_valid():
		upload = request.FILES.get('code', None)
		task = get_object_or_404(Task, url=task_url)
		user = request.user.id
		print user
		user = get_object_or_404(UserProfile, id=user)
		date = datetime.now()
		sub = Submission(task=task, code=upload, date=date, user=user)
		sub.save()
		judge = Submission_judge(sub=sub)
		judge.save()
		context_dict['judge'] = judge
	else:
		request.session['error_message'] = "Upload file wasn't chosen"
	print("sarma %d" % sub.id)
	return redirect('lark:submission', task=task_url, sub_id=sub.id)

def list_test_result(request):
	sub_id = request.GET['sub_id']
	submission = get_object_or_404(Submission, id=sub_id)
	result_test = Submission_test.objects.filter(sub_id=sub_id).order_by('series', 'index')

	data = [Submission_testSerializer(test).data for test in result_test]
	sub = SubmissionSerializer(submission).data
	sub['date'] = strftime('%Y-%m-%d %H:%M');
	return JsonResponse({'results': data, 'sub': sub})

def submission(request, task, sub_id):
	submission = get_object_or_404(Submission, id=sub_id)
	result_test = Submission_test.objects.filter(sub_id=sub_id).order_by('series', 'index')
	user = submission.user
	task = submission.task
	cnt = -1
	prev = -1
	result = []
	for i in result_test:
		if prev != i.series:
			result.append([])
			cnt += 1
		result[cnt].append(i)
		prev = i.series
	code = open(submission.code.url).read()
	context_dict = {'sub': submission, 'code': code, 'results': result, 'user': user, 'task': task}
	return render(request, 'lark/submission.html', context_dict)

@login_required	
def my_user(request):
	user_id = request.user.id
	user = get_object_or_404(UserProfile, id=user_id)
	subs = Submission.objects.filter(user=user, verdict='ACCEPTED').distinct('task_id')
	print subs[0]
	tasks = []
	context_dict = {'user': user, 'subs': subs}
	return HttpResponse("NINJA")
	return render(request, 'lark/my_user.html', context_dict)

def user_login(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(username=username, password=password)

		if user:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect('/paas/')
			else:
				return HttpResponse("Account disabled.")
		else:
			print "Invalid login details: {0}, {1}".format(username, password)
			return HttpResponse("Invalid login details supplied.")

	else:
		return render(request, 'lark/login.html', {})

@login_required
def user_logout(request):
	logout(request)

	return HttpResponseRedirect('/paas/')

def register(request):
	#is registration successful
	registered = False

	if request.method == 'POST':
		user_form = UserForm(data=request.POST)
		profile_form = UserProfileForm(data=request.POST)

		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save()

			#hash password
			user.set_password(user.password)
			user.save()

			# commit = False - we need to set the user attribute ourselves
			profile = profile_form.save(commit=False)
			profile.user = user

			profile.save()

			registered = True

		# Invalid form
		else:
			print user_form.errors, profile_form.errors

	else:
		user_form = UserForm()
		profile_form = UserProfileForm()

	return render(request,
			'lark/register.html',
			{'user_form': user_form, 'profile_form': profile_form, 
			 'registered': registered}
			 )
