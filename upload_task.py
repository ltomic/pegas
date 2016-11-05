import os, sys
import re
import json
import django
sys.path.append(os.path.dirname(
			os.path.dirname(os.path.realpath(__file__)))
		)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pegas.settings")
django.setup()

from info.var import (
    BASE_DIR,
    )

import lark.compiler as compiler

from tasks.models import Task, TestCase

def insert_test_case(tests, task, folder, dummy, p):
    for i in tests:
        out = i.replace("in", "out")
        m = p.match(i)
        test_case = TestCase(ulaz=folder+i, izlaz=folder+out, 
            task_id=task.id, index=m.group(1), is_dummy=dummy)
        test_case.save()

def upload(name):
    global BASE_DIR
    lang_info = json.load(open(BASE_DIR + "info/lang.json", 'r'))
    task_folder = BASE_DIR + "test/" + name + "/"
    folder = os.listdir(task_folder)
	
    dummy_pattern = re.compile("{}.dummy.in.[0-9a-b]+".format(name))
    test_pattern = re.compile("{}.in.[0-9a-b]+".format(name))

    dummy = []
    test = []
    limits = json.load(open(task_folder + "{}.json".format(name), 'r'))

    for i in folder:
        if dummy_pattern.match(i):
            dummy.append(i)
        if test_pattern.match(i):
	    test.append(i)

    task = Task(name=name, link='',
		time_limit=limits['limits']['time'], 
                memory_limit=limits['limits']['memory'],
		url=name, checker='test/'+name+'/checker',
		checker_lang=limits['checker_lang'], tip=0)
    task.save()
  
    print type(task.checker)
    print(compiler.compilecode(
        str(task.checker) + '.' + lang_info[task.checker_lang]['ext'],
        str(task.checker), task.checker_lang, lang_info[task.checker_lang]['ext'])
        )
    p = re.compile('{}.dummy.in.([0-9a-z]+)'.format(name))
    insert_test_case(dummy, task, task_folder, False, p)
    p = re.compile('{}.in.([0-9a-z]+)'.format(name))
    insert_test_case(test, task, task_folder, True, p)

if __name__ == "__main__":
	upload(sys.argv[1])
