CC=g++-4.8
SRCDIR=src
BINDIR=bin

CFLAGS=-std=c++11 -O2

$(BINDIR):
		mkdir -p $(BINDIR)

run_code: $(SRCDIR)/run_code.cpp | $(BINDIR)
		$(CC) $(CFLAGS) $(SRCDIR)/run_code.cpp -w -o lark/sandbox/bin/run_code
