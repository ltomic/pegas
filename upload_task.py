import os, sys
import re
import json as simplejson
import django
sys.path.append(os.path.dirname(
			os.path.dirname(os.path.realpath(__file__)))
		)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pegas.settings")
django.setup()
from tasks.models import Task, TestCase

def upload(name):
	BASE_DIR = os.path.dirname(__file__)
	PATH = BASE_DIR
	if len(BASE_DIR) != 0:
		PATH += '/'
	PATH += "test/" + name + "/"
	folder = os.listdir(PATH)
	
	dummy_pattern = re.compile("{}.dummy.in.[0-9a-b]+".format(name))
	test_pattern = re.compile("{}.in.[0-9a-b]+".format(name))

	dummy = []
	test = []
	limits = file(PATH + "{}.json".format(name)).read()

	limits = simplejson.loads(limits)

	for i in folder:
		if dummy_pattern.match(i):
			dummy.append(i)
		if test_pattern.match(i):
			test.append(i)

	task = Task(
		name=name, link='',
		time_limit=limits['time_limit'], memory_limit=limits['memory_limit'],
		url=name, checker='test/'+name+'/checker',
		checker_lang='py', tip=0)
	task.save()

	p = re.compile('{}.dummy.in.([0-9a-z]+)'.format(name))
	for i in dummy:
		out = i.replace("in", "out")
		m = p.match(i)
		test_case = TestCase(
			ulaz=PATH+i, izlaz=PATH+out,
			task_id = task.id, index=m.group(1), is_dummy=False)
		test_case.save()

	p = re.compile('{}.in.([0-9a-z]+)'.format(name))
	for i in test:
		out = i.replace("in", "out")
		m = p.match(i)
		test_case = TestCase(
			ulaz=PATH+i, izlaz=PATH+out,
			task_id = task.id, index=m.group(1), is_dummy=True)
		test_case.save()

if __name__ == "__main__":
	upload(sys.argv[1])
