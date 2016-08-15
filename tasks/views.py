from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from user.models import UserProfile
from tasks.models import Task

from tasks.serializers import TaskSerializer

@login_required
def index(request):
	task_list = Task.objects.all().order_by('name')
        print (request.user, request.user.id)
        user = UserProfile.objects.get(id=request.user.id)
	context_dict = {'tasks': task_list, 'user': user}
	return render(request, 'tasks/index.html', context_dict)

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
