import matplotlib.pyplot as plt


averageWaitingTime = [0, 0, 0, 0, 0]
averageResponseTime = [0, 0, 0, 0, 0]
averageTurnAroundTime = [0, 0, 0, 0, 0]
averageCPU_utilization = [0, 0, 0, 0, 0]
averageContextSwitch = [0, 0, 0, 0, 0]

averageWaitingTime1 = [0, 0, 0, 0, 0]
averageResponseTime1 = [0, 0, 0, 0, 0]
averageTurnAroundTime1 = [0, 0, 0, 0, 0]
averageCPU_utilization1 = [0, 0, 0, 0, 0]
averageContextSwitch1 = [0, 0, 0, 0, 0]

numberOfTestcases = 17
timeslotParameters = [1, 2, 3, 5, 8]
memorySizes = [64, 128, 256, 512]

def readScheduleFile(fileName):
    f = open(fileName, "r")
    waitingTime = 0
    responseTime = 0
    turnAroundTime = 0
    numberOfProcs = 0
    utilization = 0
    contextSwitch = 0
    for line in f:
        data = line.split(' ')
        if len(data) == 5:
            if int(data[3]) >= 0:
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
    hitTimes = 0
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
                sumTotalFreeSize += int(freeAndUsedSize.split(' ')[0])
                if len(freeRegionAfter) > 1:
                    freeRegions = freeRegionAfter.split(' ')
                    freeRegionsInt = [int(x) for x in freeRegions if x.isdigit()]
                    sumAverageFreeButCannotAllocated += sum(freeRegionsInt) / len(freeRegionsInt)
                else:
                    sumAverageFreeButCannotAllocated += 0
        counter = (counter + 1) % 4
    hitTimes = int(freeAndUsedSize.split(' ')[0])
    missTimes = int(freeAndUsedSize.split(' ')[1])

    return (hitTimes, missTimes, sumAverageFreeButCannotAllocated, sumTotalFreeSize)


if __name__ == '__main__':
    for memory in memorySizes:
        totalMissTimes = 0
        totalFreeNotEnough = 0
        totalFreeSize = 0
        totalMissTimes1 = 0
        totalFreeNotEnough1 = 0
        totalFreeSize1 = 0
        readFile = 0
        for j in range(len(timeslotParameters)):
            for i in range(1, numberOfTestcases + 1):
                readFile += 1

                fileName = "output" + str(i) + "_" + str(timeslotParameters[j]) + ".txt"
                print("./first_fit/" + str(memory) + "/memory/" + fileName)
                #(t, r, w, u, c) = readScheduleFile("./first_fit/" + str(memory) + "/schedule/" + fileName)
                (h, m, freeNotEnough, totalFree) = readMemoryFile("./first_fit/" + str(memory) + "/memory/" + fileName)

                totalMissTimes += m
                if m > 0:
                    totalFreeNotEnough += freeNotEnough / m
                    totalFreeSize += totalFree / m
                #print(" Miss times: {miss}, freeNotUsed: {f} , total Free: {tf}".format(miss=m, f=freeNotEnough, tf=totalFree))

                # averageTurnAroundTime[j] += t
                # averageResponseTime[j] += r
                # averageWaitingTime[j] += w
                # averageCPU_utilization[j] += u
                # averageContextSwitch[j] += c

                print("./best_fit/" + str(memory) + "/memory/" + fileName)
                # (t, r, w, u, c) = readScheduleFile("./best_fit/" + str(memory) + "/schedule/" + fileName)
                (h, m, freeNotEnough, totalFree) = readMemoryFile("./best_fit/" + str(memory) + "/memory/" + fileName)
                #print(" Miss times: {miss}, freeNotUsed: {f} , total Free: {tf}".format(miss=m, f=freeNotEnough, tf=totalFree))
                totalMissTimes1 += m
                if m > 0:
                    totalFreeNotEnough1 += freeNotEnough / m
                    totalFreeSize1 += totalFree / m
                # averageTurnAroundTime1[j] += t
                # averageResponseTime1[j] += r
                # averageWaitingTime1[j] += w
                # averageCPU_utilization1[j] += u
                # averageContextSwitch1[j] += c

        #     averageTurnAroundTime[j] /= numberOfTestcases
        #     averageResponseTime[j] /= numberOfTestcases
        #     averageWaitingTime[j] /= numberOfTestcases
        #     averageContextSwitch[j] /= numberOfTestcases
        #     averageCPU_utilization[j] /= numberOfTestcases
        #
        #     averageTurnAroundTime1[j] /= numberOfTestcases
        #     averageResponseTime1[j] /= numberOfTestcases
        #     averageWaitingTime1[j] /= numberOfTestcases
        #     averageContextSwitch1[j] /= numberOfTestcases
        #     averageCPU_utilization1[j] /= numberOfTestcases
        #
        # line1, = plt.plot(timeslotParameters, averageTurnAroundTime, label='Turn Around Time')
        # line2, = plt.plot(timeslotParameters, averageResponseTime, label='Response Time')
        # line3, = plt.plot(timeslotParameters, averageWaitingTime, label='Waiting Time')
        # line4, = plt.plot(timeslotParameters, averageContextSwitch, label='Context Switch')
        # plt.legend(handles=[line1, line2, line3, line4])
        # plt.title("Statistic of CPU scheduler with FCFS and RR")
        # plt.xlabel("Time slot (s)")
        # plt.ylabel("Second")
        #
        # plt.savefig("./first_fit/" + str(memory) + "/statistic.png")
        #
        # line1, = plt.plot(timeslotParameters, averageTurnAroundTime1, label='Turn Around Time')
        # line2, = plt.plot(timeslotParameters, averageResponseTime1, label='Response Time')
        # line3, = plt.plot(timeslotParameters, averageWaitingTime1, label='Waiting Time')
        # line4, = plt.plot(timeslotParameters, averageContextSwitch1, label='Context Switch')
        # plt.legend(handles=[line1, line2, line3, line4])
        # plt.title("Statistic of CPU scheduler with FCFS and RR")
        # plt.xlabel("Time slot (s)")
        # plt.ylabel("Second")
        #
        # plt.savefig("./best_fit/" + str(memory) + "/statistic.png")
        #
        # averageResponseTime = [0, 0, 0, 0, 0]
        # averageTurnAroundTime = [0, 0, 0, 0, 0]
        # averageCPU_utilization = [0, 0, 0, 0, 0]
        # averageContextSwitch = [0, 0, 0, 0, 0]
        #
        # averageWaitingTime1 = [0, 0, 0, 0, 0]
        # averageResponseTime1 = [0, 0, 0, 0, 0]
        # averageTurnAroundTime1 = [0, 0, 0, 0, 0]
        # averageCPU_utilization1 = [0, 0, 0, 0, 0]
        # averageContextSwitch1 = [0, 0, 0, 0, 0]
        totalMissTimes /= readFile
        totalFreeNotEnough /= readFile
        totalFreeSize /= readFile

        totalMissTimes1 /= readFile
        totalFreeNotEnough1 /= readFile
        totalFreeSize1 /= readFile

        plt.title("Statistic of first fit and best fit algorithms")
        plt.bar([2, 7], [totalFreeNotEnough, totalFreeSize], color='orange', width=0.25,
                edgecolor='grey', label='First Fit')
        plt.bar([3, 8], [totalFreeNotEnough1, totalFreeSize1], color='b', width=0.25,
                edgecolor='grey', label='Best Fit')
        plt.xticks([2.5, 7.5],
                   ['Average free memory\n in each segment', 'Average \n total free memory'])

        plt.legend()
        plt.ylabel("Bytes")
        #plt.show()
        plt.savefig("memory_statistic_" + str(memory) + ".png")
        plt.clf()

        plt.bar([0], [totalMissTimes], color='orange', width=0.25,
                edgecolor='grey', label='First Fit')
        plt.bar([5], [totalMissTimes1], color='b', width=0.25,
                edgecolor='grey', label='Best Fit')
        plt.title("Number of times cannot allocate memory")
        plt.legend()
        plt.ylabel("Times")
        #plt.show()
        plt.savefig("miss_times_" + str(memory) + ".png")
        plt.clf()
