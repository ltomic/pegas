#include <cstdio>
#include <cstdlib>
#include <string>
#include <iostream>
#include <unistd.h>
#include <err.h>
#include <sys/resource.h>
#include <cmath>
#include <sys/stat.h>
#include <cstring>
#include <sys/wait.h>
#include <fcntl.h>

using namespace std;

double time_limit;
int memory_limit;

FILE *info, *errors;

void read_limits(char time[], char mem[]) {
	sscanf(time, "%lf", &time_limit);
	sscanf(mem, "%d", &memory_limit);
}

void open_file(FILE *&f, string path, bool t) {
	if ((f = fopen(path.c_str(), (t == 0) ? "r" : "w")) == NULL) {
		string err = "file open error " + path + "\n";
		perror(err.c_str());
		exit(0);
	}
}

double get_time_usage(pid_t pid) {
	int fd;
	long long t=0;
	char buff[8192];
	sprintf(buff, "/proc/%d/stat", pid);
	if ((fd = open(buff, O_RDONLY)) < 0) {
		return -1;
	}
	read(fd, buff, 8191);
	close(fd);
	int i = 0;
	for (int cnt = 0; buff[i] && cnt < 13; ++i) {
		if (buff[i] == ' ') cnt++;
	}
	for (; buff[i]; ++i) {
		if (buff[i] == ' ') break;
		t = t * 10 + buff[i] - '0';
	}
	return (double)t / sysconf(_SC_CLK_TCK);
}

int get_memory_usage(pid_t pid) {
	int fd, data, stack;
	char buff[8192], *p, *q;
	p = buff;
	sprintf(p, "/proc/%d/status", pid);
	if ((fd = open(p, O_RDONLY)) < 0) {
		return -1;
	}

	read(fd, p, 8191);
	close(fd);

	data = stack = 0;
	q = strstr(p, "VmData:");
	if (q != NULL) {
		sscanf(q, "%*s %d", &data);
		q = strstr(q, "VmStk:");
		sscanf(q, "%*s %d\n", &stack);
	}
	return (data + stack);
}

void parent(int pid) {
	pid_t pid2;
	int status = 0, memory_used = 128;
	double time_used = 0;
	do {
		pid2 = waitpid(pid, &status, WUNTRACED | WNOHANG);
		memory_used = max(memory_used, get_memory_usage(pid));
		time_used = max(time_used, get_time_usage(pid));
		if (pid2 == -1) {
			perror("waitpid");
			exit(EXIT_FAILURE);
		}
		int signal = WIFSIGNALED(status) ? WTERMSIG(status) : 0;
	} while (pid2 == 0);

	fprintf(info, "\"signal\" : \"%d\",\n", WTERMSIG(status));
	fprintf(info, "\"memory\" : \"%.2f\",\n", memory_used / 1024.0);
	fprintf(info, "\"time\" : \"%lf\"\n", time_used);
}

void child(FILE *in, FILE *out) {
	dup2(fileno(in), STDIN_FILENO);
	dup2(fileno(out), STDOUT_FILENO);
	fclose(in);
	fclose(out);
	struct rlimit limit;
	getrlimit(RLIMIT_CPU, &limit);
	limit.rlim_cur = (int)ceil(time_limit);
	setrlimit(RLIMIT_CPU, &limit);

	getrlimit(RLIMIT_AS, &limit);
	limit.rlim_cur = limit.rlim_max = memory_limit * 1024L * 1024L;
	setrlimit(RLIMIT_AS, &limit);
	char *const argv[] = {"lark/sandbox/code", 0};
	char *envp [] = {
		"HOME=/usr/home/prog/pegas/lark/sandbox",
		"PATH=./",
		"USER=ltomic",
		"LOGNAME=ltomic",
		"PWD=./",
		"OLDPWD=./",
		0
	};
	execve(argv[0], &argv[0], envp);
	perror("execve");
	_exit(1);
}

void run_test() {
	int pid;
	FILE *in, *out;

	open_file(in, "lark/sandbox/tests/in", 0);
	open_file(out, "lark/sandbox/ans", 1);
	if ((pid = fork()) == -1) {
		perror("fork");
	}
	if (pid != 0) {
		parent(pid);
	} else {
		child(in, out);
	}
	fclose(in);
	fclose(out);
}

int main(int argc, char **argv) {
	open_file(info, "lark/sandbox/info.json", 1);
	fprintf(info, "{\n");
	open_file(errors, "lark/sandbox/errors", 1);
	read_limits(argv[1], argv[2]);
	run_test();
	fprintf(info, "}");
	fclose(info);
	fclose(errors);
	return 0;
}
