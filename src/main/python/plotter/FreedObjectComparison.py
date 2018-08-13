import matplotlib.pyplot as plt
from matplotlib import gridspec
import matplotlib.dates as mdates
import matplotlib as mpl
import os, sys

from datetime import datetime
from reader import FileReader
from statistics.GCActivities import GCActivities



class HeapUsage:
    def __init__(self, gcActivities):
        self.gcActivities = gcActivities

    def getUsageAndTime (self):
        timeList = []
        usedList = []
        for gcEvent in gcActivities.gcEvents:
            timeList.append(gcEvent.time)
            usedList.append(gcEvent.used)
        return (timeList, usedList)

    def getAllocatedAndTime(self):
        timeList = []
        allocatedList = []
        for gcEvent in gcActivities.gcEvents:
            timeList.append(gcEvent.time)
            allocatedList.append(gcEvent.allocated)
        return (timeList, allocatedList)

    def getGCPauseAndTime(self, gcCause):
        timeList = []
        gcPauseList = []

        for gcEvent in gcActivities.gcEvents:
            if (gcEvent.gcCause == gcCause):
                timeList.append(gcEvent.time)
                gcPauseList.append(gcEvent.gcPauseTime)

        return (timeList, gcPauseList)

    def getFreedNonLargeObjNumsAndTime(self):
        timeList = []
        freedObjNumList = []
        totalFreedObjNum = 0

        for gcEvent in gcActivities.gcEvents:
            timeList.append(gcEvent.time)
            totalFreedObjNum += gcEvent.freedObjNum
            freedObjNumList.append(totalFreedObjNum)

        return (timeList, freedObjNumList)


    def getFreedNonLargeObjSizesAndTime(self):
        timeList = []
        freedObjSizeList = [] #MB
        totalFreedObjSize = 0

        for gcEvent in gcActivities.gcEvents:
            timeList.append(gcEvent.time)
            totalFreedObjSize += gcEvent.freedObjSize
            freedObjSizeList.append(totalFreedObjSize)

        return (timeList, freedObjSizeList)

    def getFreedLargeObjNumsAndTime(self):
        timeList = []
        freedObjNumList = []
        totalFreedObjNum = 0

        for gcEvent in gcActivities.gcEvents:
            timeList.append(gcEvent.time)
            totalFreedObjNum += gcEvent.largeObjNum
            freedObjNumList.append(totalFreedObjNum)

        return (timeList, freedObjNumList)


    def getFreedLargeObjSizesAndTime(self):
        timeList = []
        freedObjSizeList = [] #MB
        totalFreedObjSize = 0

        for gcEvent in gcActivities.gcEvents:
            timeList.append(gcEvent.time)
            totalFreedObjSize += gcEvent.largeObjSize
            freedObjSizeList.append(totalFreedObjSize)

        return (timeList, freedObjSizeList)

    def getFreedAvgLargeObjSizesAndTime(self):
        timeList = []
        freedObjSizeList = [] #MB

        for gcEvent in gcActivities.gcEvents:
            if (gcEvent.largeObjNum != 0):
                timeList.append(gcEvent.time)
                freedObjSizeList.append(gcEvent.largeObjSize / gcEvent.largeObjNum)

        return (timeList, freedObjSizeList)


def plotHeapUsage(appName, title, gcActivities):



    heapUsage = HeapUsage(gcActivities)

    fig, axes = plt.subplots(nrows=2, ncols=1, sharey=False, sharex=True, figsize=(6.3, 4.5))

    plt.rc('font', family='Helvetica', size=12)

    plt.subplots_adjust(left=0.11, bottom=0.12, right=0.96, top=0.92,
                        wspace=0.2, hspace=0.08)
    #gs = gridspec.GridSpec(3, 1)
    #axes[0] = plt.subplot(gs[0, :3])
    # identical to ax1 = plt.subplot(gs.new_subplotspec((0,0), colspan=3))
    #axes[1] = plt.subplot(gs[2:, :])


    axes[0].set_ylabel("Non-large Objects (MB)")
    axes[1].set_ylabel("Large Objects (MB)")
    axes[1].set_xlabel("Time (s)")
    # axes[0].set_ylim(0, 400)  # The ceil
    # axes[1].set_ylim(0, 65)
    # axes[2].set_ylim(0, 400)

    # axes[1].set_ylim(0, 40)  # The ceil


    freedObjSize = heapUsage.getFreedNonLargeObjSizesAndTime()
    freedObjSizeLine = axes[0].plot(freedObjSize[0], freedObjSize[1], 'o-', linewidth=1.5, markersize=2, label='Freed Non-large Object Size')
    axes[0].legend(frameon=False)

    freedLargeObjSize = heapUsage.getFreedLargeObjSizesAndTime()
    freedLargeObjSizeLine = axes[1].plot(freedLargeObjSize[0], freedLargeObjSize[1], 'o-', linewidth=1.5, markersize=2, label='Freed Large Object Size')
    freedAvgLargeObjSize = heapUsage.getFreedAvgLargeObjSizesAndTime()
    freedAvgLargeObjSizeLine = axes[1].bar(freedAvgLargeObjSize[0], freedAvgLargeObjSize[1], 0.5, color='red', label='Freed Average Large Object Size')

    axes[1].legend(frameon=False)


    #
    # axes[0].grid(False)
    # axes[1].grid(False)
    # axes[0].set_ylim(ymin=0)
    # axes[1].set_ylim(ymin=0)
    # axes[0].set_xlim(xmin=0)
    # axes[1].set_xlim(xmin=0)
    # axes[0].get_xaxis().set_visible(False)
    #
    # axes[0].legend((OldAllocatedLine, OldUsageLine),
    #                ("Allocated", "Usage"),
    #                loc='upper left', ncol=1, frameon=False)
    #
    # # draw GCPause time bar plot
    #
    # (ygcTime, ygcPause, fgcTime, fgcPause) = heapUsage.getGCPauseAndTime()
    #
    # # for i in range(1, len(ygcPause)):
    # #     ygcPause[i] = ygcPause[i-1] + ygcPause[i]
    # #
    # # for i in range(1, len(fgcPause)):
    # #     fgcPause[i] = fgcPause[i-1] + fgcPause[i]
    #
    #
    # colors2 = [u'#DDA0DD', u'#6A5ACD', u'#A9A9A9', u'#ADD8E6', u"#cc3333"]
    # #axes3 = axes[1].twinx()
    #
    #PartitalGCBar = axes[4].bar(fgcTime, fgcPause, 0.01, color=colors2[2], label="FGC Pause", edgecolor=colors2[2])
    #StrictGCBar = axes[4].bar(ygcTime, ygcPause, 0.01, color=colors2[4], label="YGC Pause", edgecolor=colors2[4])
    #
    # #axes3.set_ylabel(r"GC pause time (sec)")
    # axes[1].set_xlabel("Timeline (s)")
    # # ymin, ymax = axes[1].get_ylim()
    # # axes[1].set_ylim(ymin, ymax * 1.25)
    #
    plt.suptitle(title) #, y=0.95)
    #
    # axes[1].legend((YGCBar, FGCBar),
    #                ("YGC pause", "FGC pause"),
    #                loc='upper right', ncol=4, frameon=False)

    #plt.tight_layout()
    plt.show()

    #fig = plt.gcf()
    #plt.show()
    #fig.savefig(outputFile, dpi=300, bbox_inches='tight')




if __name__ == '__main__':

    gcLogPath = "/Users/xulijie/Documents/GCResearch/Android/logs/"


    appName = "Alexnet GC Metrics"
    gcFileName = "cnndroid_alexnet_scale1_image_time_logcat.txt"

    gcLines = FileReader.readLines(gcLogPath + gcFileName)
    gcActivities = GCActivities(gcLines)

    plotHeapUsage(appName, appName, gcActivities)

    appName = "Nin GC Metrics"
    gcFileName = "cnndroid_nin_scale1_image_time_logcat.txt"

    gcLines = FileReader.readLines(gcLogPath + gcFileName)
    gcActivities = GCActivities(gcLines)

    plotHeapUsage(appName, appName, gcActivities)
