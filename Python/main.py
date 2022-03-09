averageWaitingTime = []

pathToScheduleFolder = "../Lab4/lab4_code_sched/schedule/"
pathToMemoryFolder = "../Lab4/lab4_code_sched/memory/"
numberOfTestcases = 16 + 1
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
    for line in f:
        if counter == 0:
            freeAndUsedSize = line
        elif counter == 1:
            freeRegionsBefore = line
        elif counter == 2:
            freeRegionAfter = line
        elif counter == 3:
            allocatedSize = int(line)
            if (allocatedSize == 0):
                totalFreeSize = freeAndUsedSize.split( )[0]
                return totalFreeSize
            else:
                print(freeAndUsedSize.split( )[0])

        counter = (counter + 1) % 4

if __name__ == '__main__':
    readMemoryFile(pathToMemoryFolder + "output.txt")
    for i in range(numberOfTestcases):
        for timeslot in timeslotParameters:
            fileName = "output" + str(i) + "_" + str(timeslot) + ".txt"
            print(fileName)