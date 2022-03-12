#!/bin/bash 

for ((i = 1; i < 18; i++))
do
        for j in 1 2 3 5 8
        do
                input="input/input"$i"_"$j".txt"
               	output="output"$i"_"$j".txt"
		gcc mem.c sched.c queue.c -o sched -lpthread
		cat $input | ./sched $output
		echo `clear`
        done
done
echo "Run Successfully!"
