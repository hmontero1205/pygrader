CC=gcc
CFLAGS=-g -Wall
LDFLAGS=-g

swap: swap.o

swap.o:

.PHONY:clean
clean:
	rm -f *.o swap a.out

.PHONY: all
all: clean swap
