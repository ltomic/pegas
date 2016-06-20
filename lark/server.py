import os, shutil, sys, time, pathlib
import subprocess
import json
import django
import re
sys.path.append(os.path.dirname( ## to import pegas.settings
			os.path.dirname(os.path.realpath(__file__)))
		)


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pegas.settings")
django.setup()
from pegas import settings
from lark.models import *

os.chdir(settings.BASE_DIR)

def run_process(args):
	popen = subprocess.Popen(args, stdout=subprocess.PIPE)
	return popen.communicate()

def	check_limit(verdict, task, info):
	if verdict != 0 and verdict != 32:
		return verdict
	if task.memory_limit < float(info['memory'].encode('ascii')):
		verdict = 33 + 1 # MLE
	if task.time_limit < float(info['time'].encode('ascii')):
		verdict = 33 + 2 # TLE

	return verdict

def update_test_result(index, info, verdict):
	test_result[index].memory = info['memory']
	test_result[index].time = info['time']
	test_result[index].verdict = verdicts[str(verdict)]
	print test_result[index].verdict
	test_result[index].save()

def run_tests(task):
	global info
	shutil.copyfile(str(task.checker), 'lark/sandbox/checker')
	put = 'lark/sandbox/tests/in'
	args_judge = [
		'bin/run_code', 
		str(task.time_limit), 
		str(task.memory_limit)
		]
 	args_checker = [
		'python',
		'lark/sandbox/checker',
#		'lark/sandbox/tests/in', ## treba drugaciji checker
		'lark/sandbox/ans',
		''
		]
	for j in range(len(tests)):
		i = tests[j]
		test_result[j].verdict = "Running"
		verdict = 0
		shutil.copyfile(str(i.ulaz), put)
		run_process(args_judge)	
		if (os.stat('lark/sandbox/errors').st_size != 0):
			verdict = open('lark/sandbox/errors').read()
			verdict = int(verdict) # compile or runtime error
			info = info_error
		elif os.path.isfile('lark/sandbox/ans'):
			args_checker[3] = str(i.izlaz)
			correct_output = run_process(args_checker)[0].strip()
			correct_output = True if correct_output == 'True' else False
			info = open('lark/sandbox/info.json', 'r')
			info = json.load(info)
			verdict = check_limit(int(info['signal'].encode('ascii')), task, info)
			if verdict == 0:
				if correct_output == False:
					verdict = 33 # WA
				else:
					verdict = 32 # AC
		update_test_result(j, info, verdict)
		if (verdict != 32):
			break
		os.remove('lark/sandbox/ans')
		os.remove(put)
	return {'verdict': verdict, 'info': info}
	
def compile_code(extension):
	args_compile = ['python', 'lark/compile.py', 'lark/sandbox/code', extension]
	return run_process(args_compile)[0]

info_error = {'memory': 0, 'time': 0}
fverdicts = open("test/verdicts.json", "r")
verdicts = json.load(fverdicts)
counter = 0
verdict = 0
re_extension = re.compile(r'^.*[.](\w+)$')

while True:
	info = {}
	test_result = []
	print counter
	counter += 1
	sub_jud = Submission_judge.objects.all()
	if len(sub_jud) == 0:
		time.sleep(1.0)
		continue
	sub_jud = sub_jud[0]
	sub = sub_jud.sub
	sub.verdict = 'Running'
	sub.save()
	extension_match = re_extension.match(str(sub.code))
	extension = extension_match.group(1)
	shutil.copyfile(str(sub.code), 'lark/sandbox/code.' + extension)
	if int(compile_code(extension)) != 0:
		sub.verdict = 'Compilation error'
		sub.save()
		sub_jud.delete()
		continue
	task = sub.task
	tests = TestCase.objects.filter(task=task).order_by('-is_dummy', 'index')
	for i in tests:
		s = Submission_test(
				sub=sub, index=i.index,	
				verdict="In queue", series = (i.is_dummy+1) % 2)
		test_result.append(s)
		test_result[-1].save()

	
	result = run_tests(task)
	
	sub.verdict = verdicts[str(result['verdict'])]
	sub.time = result['info'].get('time', 0)
	sub.memory = result['info'].get('memory', 0)
	sub.save()
	sub_jud.delete()

