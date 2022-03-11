import matplotlib.pyplot as plt


averageWaitingTime = [0, 0, 0, 0, 0]
averageResponseTime = [0, 0, 0, 0, 0]
averageTurnAroundTime = [0, 0, 0, 0, 0]
averageCPU_utilization = [0, 0, 0, 0, 0]
averageContextSwitch = [0, 0, 0, 0, 0]
pathToScheduleFolder = "../Lab4/lab4_code_sched/schedule/"
pathToMemoryFolder = "../Lab4/lab4_code_sched/memory/"
numberOfTestcases = 16
timeslotParameters = [1, 2, 3, 5, 8]

def readScheduleFile(fileName):
    f = open(fileName, "r")
    waitingTime = 0
    responseTime = 0
    turnAroundTime = 0
    numberOfProcs = 0
    utilization = 0
    contextSwitch = 0
    for line in f:
        data = line.split( )
        if len(data) == 5:
            turnAroundTime += int(data[2])
            responseTime += int(data[3])
            waitingTime += int(data[4])
            numberOfProcs += 1
        elif len(data) == 2:
            utilization = float(data[0])
            contextSwitch = int(data[1])
    return (turnAroundTime / numberOfProcs, responseTime / numberOfProcs, waitingTime / numberOfProcs, utilization, contextSwitch)

def readMemoryFile(fileName):
    f = open(fileName, "r")
    counter = 0
    freeAndUsedSize = ""
    freeRegionsBefore = ""
    freeRegionAfter = ""
    allocatedSize = 0
    missTimes = 0
    sumTotalFreeSize = 0
    sumAverageFreeButCannotAllocated = 0
    for line in f:
        if counter == 0:
            freeAndUsedSize = line
        elif counter == 1:
            freeRegionsBefore = line
        elif counter == 2:
            freeRegionAfter = line
        elif counter == 3:
            allocatedSize = int(line)
            if allocatedSize == 0:
                missTimes += 1
                totalFreeSize = int(freeAndUsedSize.split(' ')[0])
                sumTotalFreeSize += totalFreeSize
                freeRegions = freeRegionAfter.split(' ')
                freeRegionsInt = [int(x) for x in freeRegions if x.isdigit()]
                sumAverageFreeButCannotAllocated += sum(freeRegionsInt) / len(freeRegionsInt)
        counter = (counter + 1) % 4

    return (missTimes, sumAverageFreeButCannotAllocated, sumTotalFreeSize)

if __name__ == '__main__':
    readFile = 0
    for j in range(len(timeslotParameters)):
        for i in range(1, numberOfTestcases + 1):
            readFile += 1
            fileName = "output" + str(i) + "_" + str(timeslotParameters[j]) + ".txt"
            (t, r, w, u, c) = readScheduleFile(pathToScheduleFolder + fileName)
            (m, freeNotEnough, totalFree) = readMemoryFile(pathToMemoryFolder + fileName)
            print(" Miss times: {miss}, freeNotUsed: {f} , total Free: {tf}".format(miss=m, f=freeNotEnough, tf=totalFree))
            averageTurnAroundTime[j] += t
            averageResponseTime[j] += r
            averageWaitingTime[j] += w
            averageCPU_utilization[j] += u
            averageContextSwitch[j] += c
        averageTurnAroundTime[j] /= numberOfTestcases
        averageResponseTime[j] /= numberOfTestcases
        averageWaitingTime[j] /= numberOfTestcases
        averageContextSwitch[j] /= numberOfTestcases
        averageCPU_utilization[j] /= numberOfTestcases

    line1, = plt.plot(timeslotParameters, averageTurnAroundTime, label='Turn Around Time')
    line2, = plt.plot(timeslotParameters, averageResponseTime, label='Response Time')
    line3, = plt.plot(timeslotParameters, averageWaitingTime, label='Waiting Time')
    line4, = plt.plot(timeslotParameters, averageContextSwitch, label='Context Switch')
    plt.legend(handles=[line1, line2, line3, line4])
    plt.title("Statistic of CPU scheduler with FCFS and RR")
    plt.xlabel("Time slot (s)")
    plt.ylabel("Second")
    #plt.plot(timeslotParameters, averageTurnAroundTime,  timeslotParameters, averageResponseTime, timeslotParameters, averageWaitingTime, timeslotParameters, averageContextSwitch)
    plt.savefig("statistic.png")
    print(sum(averageCPU_utilization) / len(averageCPU_utilization))
    print("Number of file to be read: {files}".format(files=readFile))