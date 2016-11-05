import sys, os, shutil
import subprocess

def run_process(args):
	popen = subprocess.Popen(args, stdout=subprocess.PIPE)
	return popen.communicate()[0]


# src - put do source koda
def compilecode(src, exe, lang, extension):
    args = {
        'C++': ['g++-4.8', src + '.'+extension , '-o', exe],
        'Python 2': [],
        'Python 3': [],
    }
    print src, exe
    sys.stdout.write('File check...')
    if os.path.isfile(src) == True:
        print "OK!"
    else:
        print "Fail!"
        return '1'
    if len(args[lang]) != 0:
        return len(run_process(args[lang]))
    else:
        shutil.copyfile(src, exe)
        return '0'
