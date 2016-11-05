import os, shutil, sys, time, pathlib
import subprocess
import json
import django
import re

from lark.compiler import compilecode

sys.path.append(os.path.dirname( ## to import pegas.settings
			os.path.dirname(os.path.realpath(__file__)))
		)


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pegas.settings")
django.setup()
from pegas import settings
from tasks.models import (
        TestCase
        )

from lark.models import (
    Submission,
    Submission_judge,
    Submission_test,
    )

os.chdir(settings.BASE_DIR)

from info.var import (
    info_error,
    info_lang,
    path,
    argv_lang,
    verdicts,
    args_judge,
    )

def run_process(args, cwd):
    popen = subprocess.Popen(args, stdout=subprocess.PIPE, shell=False, cwd=cwd)
    return popen.communicate()

def check_limit(verdict, task, info):
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
    test_result[index].save()

def run_tests(task, lang):
    shutil.copyfile(str(task.checker), path['checker'])
    args_judge.extend([str(task.time_limit), str(task.memory_limit),
                       argv_lang[lang]])
    args_checker = [
        info_lang[task.checker_lang]['run'],
	'lark/sandbox/ans',
        ''
    ]
    if args_checker[0] == 'bin':
        args_checker[0] = './' + path['checker']
    else:
        args_checker.insert(1, path['checker'])
    
    for j in range(len(tests)):
	test = tests[j]
	test_result[j].verdict = "Running"
	verdict = 0
	shutil.copyfile(str(test.ulaz), path['input'])
	run_process(args_judge, '/')[0]
        verdict = open(path['error']).read()

        if len(verdict) != 0 or os.path.isfile('lark/sandbox/ans') == False:
            verdict = int(verdict) # compile or runtime error
	    info = info_error
	else:
	    args_checker[-1] = str(test.izlaz)
            correct_output = run_process(args_checker, '.')[0].strip()
	    correct_output = correct_output == 'True'
	    info = json.load(open(path['usage'], 'r'))
            os.remove(path['usage'])
	    verdict = check_limit(int(info['signal']), task, info)
	    if verdict == 0:
	        if correct_output == False:
	            verdict = 33 # WA
		else:
                    verdict = 32 # AC
	update_test_result(j, info, verdict)
	os.remove(path['ans'])
	os.remove(path['input'])
	if (verdict != 32):
	    break
    return {'verdict': verdict, 'info': info}
	
def insert_tests(sub, tests):
    for test in tests:
        s = Submission_test(sub=sub, index=test.index, verdict="In queue", 
                            series = (test.is_dummy+1)%2
            )
        test_result.append(s)
    for i in test_result:
        i.save()

def update_submission(sub, result):
    sub.verdict = verdicts[str(result['verdict'])]
    sub.time = result['info'].get('time', 0)
    sub.memory = result['info'].get('memory', 0)
    sub.save()

def compile_and_check(sub):
    shutil.copyfile(str(sub.code), path['code'] + '.' + sub.lang.extension)
    error = compilecode(path['code'], path['code'], 
                      sub.lang.name, sub.lang.extension)
    if int(error) != 0:
        sub.verdict = 'Compilation error'
        sub.save()
        sub_jud.delete()
        return False
    return True


counter = 0
if not os.path.exists('lark/sandbox/tests'):
    os.makedirs('lark/sandbox/tests')

while True:
    print counter
    counter += 1
    queue = Submission_judge.objects.all()
    if len(queue) == 0:
	time.sleep(1.0)
	continue
    test_result = []
    sub_jud = queue[0]
    sub = sub_jud.sub
    sub.verdict = 'Running'
    sub.save()
    
    if compile_and_check(sub) == False:
        continue

    task = sub.task
    tests = TestCase.objects.filter(task=task).order_by('-is_dummy', 'index')
        
    insert_tests(sub, tests)
    result = run_tests(task, sub.lang.name)
    
    update_submission(sub, result) 	
    sub_jud.delete()

