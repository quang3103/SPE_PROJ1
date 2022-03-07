#!/bin/bash
echo "Input file:"
cat input/input.txt
echo "Results"
gcc mem.c sched.c queue.c -o sched -lpthread
cat input/input.txt | ./sched
