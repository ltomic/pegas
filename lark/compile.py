import sys
import subprocess

def run_process(args):
	popen = subprocess.Popen(args, stdout=subprocess.PIPE)
	return popen.communicate()[0]

extension = sys.argv[2]
args = {
	'cpp': ['g++-4.9', '-std=c++11', '-w', '-O2', '-o', 
					sys.argv[1], sys.argv[1] + '.' + extension]
	}
print len(run_process(args[extension]))
