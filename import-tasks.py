import os, re, django, sys
sys.path.append(os.path.dirname(
			os.path.dirname(os.path.realpath(__file__)))
		)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pegas.settings")
django.setup()

from lark.models import Task
from upload_task import upload

re_taskname = re.compile(r'^.*[/](\w+)$')
dirs = os.walk('test')


for i in dirs:
	name = re_taskname.match(str(i[0]))
	if name == None:
		continue
	name = name.group(1)
	task = Task.objects.filter(name=name)
	if len(task) != 0:
		continue
	print name
	upload(name)
	
