
#include "queue.h"
#include "mem.h"
#include <pthread.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define TIME_UNIT	100000 // In microsecond

static struct pqueue_t in_queue; // Queue for incomming processes
static struct pqueue_t ready_queue; // Queue for ready processes

static FILE *outputFile;
static int CPUFreeTime = 0;
static int timeActuallyStart = -1;
static int contextSwitch = 0;
static int sizeOfMemory = 8; //1<<sizeOfMemory
static int load_done = 0;

static int timeslot; 	// The maximum amount of time a process is allowed
			// to be run on CPU before being swapped out

int min(int a, int b) {
	return (a < b) ? a : b;
}

// Emulate the CPU
void * cpu(void * arg) {
	int timestamp = 0;
	/* Keep running until we have loaded all process from the input file
	 * and there is no process in ready queue */
	while (!load_done || !empty(&ready_queue)) {
		/* Pickup the first process from the queue */
		struct pcb_t * proc = de_queue(&ready_queue);
		if (proc == NULL) {
			/* If there is no process in the queue then we
			 * wait until the next time slice */
			//printf("Timestamp: %d: miss\n", timestamp);
			timestamp++;
			if (timeActuallyStart != -1) CPUFreeTime++;
			usleep(TIME_UNIT);
		} else {
			/* Execute the process */
			if (timeActuallyStart == -1) {
				timeActuallyStart = timestamp;
				timestamp -= timestamp;	
			}
			int start = timestamp; 	// Save timestamp
			int id = proc->pid;	// and PID for tracking
			/* Decide the amount of time that CPU will spend
			 * on the process and write it to 'exec_time'.
			 * It should not exeed 'timeslot'.
			*/
			int exec_time = 0;

			// TODO: Calculate exec_time from process's PCB
			
			// YOUR CODE HERE
			exec_time = min(proc->burst_time, timeslot);
			
			//calculate responseTime
			if (proc->responseTime == -1) proc->responseTime = timestamp - proc->arrival_time;
			//calculate waitingTime
			proc->waitingTime += timestamp - proc->lastTimeInQueue;
			
			/* Emulate the execution of the process by using
			 * 'usleep()' function */
			usleep(exec_time * TIME_UNIT);
			
			/* Update the timestamp */
			timestamp += exec_time;

			// TODO: Check if the process has terminated (i.e. its
			// burst time is zero. If so, free its PCB. Otherwise,
			// put its PCB back to the queue.
			
			/* Track runtime status */
			//printf("%2d-%2d: Execute %d\n", start, timestamp, id);
			
			// YOUR CODE HERE
			proc->burst_time -= exec_time;
			if (proc->burst_time == 0) {
				//calculate turn around time
				int turnAroundTime = timestamp - proc->arrival_time;
				/*printf("\t **** Process ID: %d, Arrival Time: %d, Burst Time: %d, Turn Around Time: %d, Response Time: %d, Waiting Time: %d \n", proc->pid, 
																			proc->arrival_time, 
																			proc->burst_time, 
																			turnAroundTime,
																			proc->responseTime,
																			proc->waitingTime);*/
																			
				fprintf(outputFile, "%d %d %d %d %d\n", proc->pid, proc->arrival_time, turnAroundTime, proc->responseTime, proc->waitingTime);
				mem_free(proc->mem);
				free(proc);
				//printf("Process exectuion is done, free memory\n");
			} else {
				proc->lastTimeInQueue = timestamp;
				en_queue(&ready_queue, proc);
			}
			//count for context switch
			contextSwitch += 1;
		}
	}
	//printf("CPU free time: %d, Complete Time: %d, CPU Utilization(%): %f\n", CPUFreeTime, timestamp, (double)(timestamp - CPUFreeTime)/timestamp);
	//printf("Context switch: %d times\n", contextSwitch);
	fprintf(outputFile, "%0.3f %d\n", (double)(timestamp - CPUFreeTime)*100/timestamp, contextSwitch);
	return NULL;
}

// Emulate the loader
void * loader(void * arg) {
	int timestamp = 0;
	/* Keep loading new process until the in_queue is empty*/
	while (!empty(&in_queue)) {
		struct pcb_t * proc = de_queue(&in_queue);
		/* Loader sleeps until the next process available */
		int wastetime = proc->arrival_time - timestamp;
		usleep(wastetime * TIME_UNIT);
		/* Update timestamp and put the new process to ready queue */
		timestamp += wastetime;
		void* mem = mem_alloc(proc->burst_time*4);
		if (mem) {
			proc->mem = mem;
			proc->lastTimeInQueue = timestamp;
			proc->waitingTime = 0;
			proc->responseTime = -1;
			en_queue(&ready_queue, proc);
		}
		//printf("Timestamp: %d | Process ID: %d\n", timestamp, proc->pid);
	}
	/* We have no process to load */
	load_done = 1;

	return NULL;
}

/* Read the list of process to be executed from stdin */
void load_task() {
	int num_proc = 0;
	scanf("%d %d\n", &timeslot, &num_proc);
	int i;
	for (i = 0; i < num_proc; i++) {
		struct pcb_t * proc =
			(struct pcb_t *)malloc(sizeof(struct pcb_t));
		scanf("%d %d\n", &proc->arrival_time, &proc->burst_time);
		proc->pid = i;
		proc->numberOfBytes = proc->burst_time;
		en_queue(&in_queue, proc);
	}
}

int main(int argc, const char *argv[]) {
	//printf("argc : %d | FILE NAME: %s\n", argc, argv[1]);
	char fileNameFromCMD[30];
	strcpy(fileNameFromCMD, "schedule/");
	strcat(fileNameFromCMD, argv[1]);
	printf("File name: %s\n", fileNameFromCMD);
	outputFile = fopen(fileNameFromCMD, "w");
	pthread_t cpu_id;	// CPU ID
	pthread_t loader_id;	// LOADER ID

	/* Initialize queues */
	initialize_queue(&in_queue);
	initialize_queue(&ready_queue);
	mem_init(1<<sizeOfMemory, argv[1]);

	/* Read a list of jobs to be run */
	load_task();

	/* Start loader */
	pthread_create(&loader_id, NULL, loader, NULL);
	/* Start cpu */
	pthread_create(&cpu_id, NULL, cpu, NULL);

	/* Wait for cpu and loader */
	pthread_join(loader_id, NULL);
	pthread_join(cpu_id, NULL);
	
	mem_finish();
	pthread_exit(NULL);

}


