import sys
from django.shortcuts import (
        render, redirect,
        get_object_or_404, get_list_or_404, 
        )
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
        Submission_judge, Submission, Submission_test, 
        Language
        )
from tasks.models import Task, TestCase
from lark.forms import CodeForm
from lark.serializers import SubmissionSerializer, Submission_testSerializer

from user.models import UserProfile

def list_submissions(request):
    print "gla"
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
    code_form = CodeForm()
    task = get_object_or_404(Task, url=task_url)
    user = get_object_or_404(UserProfile, id=request.user.id)
    subs = Submission.objects.filter(user=user, task=task).order_by('-date')[:5]
    upload_error = request.session.pop('error_message', None)
    context_dict = {
    	'user': user,
    	'task': task,
    	'code_form': code_form,
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
        lang = request.POST.get('lang', None)
        lang = Language.objects.filter(name=lang)[0]
        task = get_object_or_404(Task, url=task_url)
        user = request.user.id
	print user
	user = get_object_or_404(UserProfile, id=user)
	date = datetime.now()
	sub = Submission(
                task=task, code=upload, date=date, user=user, lang=lang
                )
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
    print "Da"
    print sub_id
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

