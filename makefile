CC=g++-4.9
SRCDIR=src
BINDIR=bin

CFLAGS=-std=c++11 -O2

$(BINDIR):
		mkdir -p $(BINDIR)

run_code: $(SRCDIR)/run_code.cpp | $(BINDIR)
		$(CC) $(CFLAGS) $(SRCDIR)/run_code.cpp -w -o $(BINDIR)/run_code