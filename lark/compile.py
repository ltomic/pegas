import sys
import subprocess

def run_process(args):
	popen = subprocess.Popen(args, stdout=subprocess.PIPE)
	return popen.communicate()[0]

lang = sys.argv[2]
extension = sys.argv[3]
args = {
	'C++': ['g++-4.9', '-std=c++11', '-w', '-O2', '-o', 
		sys.argv[1], 'lark/sandbox/code.' + extension],
        'Python 2': [],
        'Python 3': [],
	}
if len(args[lang]) != 0:
    print len(run_process(args[lang]))
else:
    print '0'
