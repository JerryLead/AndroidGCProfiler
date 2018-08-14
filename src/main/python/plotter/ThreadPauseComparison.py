import matplotlib.pyplot as plt
from matplotlib import gridspec
import matplotlib.dates as mdates
import matplotlib as mpl
import os, sys
import numpy as np

from datetime import datetime
from reader import FileReader
from statistics.GCActivities import GCActivities


# ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
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

    def getAccumulatedGCPauseAndTime(self):
        timeList = []
        gcPauseList = []
        gcPause = 0

        for gcEvent in gcActivities.gcEvents:
            gcPause += gcEvent.gcPauseTime
            timeList.append(gcEvent.time)
            gcPauseList.append(gcPause)

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

    def getConcurrentGCAndTime(self, gcCause):
        timeList = []
        gcTotalTimeList = []

        for gcEvent in gcActivities.gcEvents:
            if (gcEvent.gcCause == gcCause):
                timeList.append(gcEvent.time)
                gcTotalTimeList.append(gcEvent.gcTotalTime - gcEvent.gcPauseTime)

        return (timeList, gcTotalTimeList)

    def getThreadPauseAndTime(self):
        timeList = []
        threadPauseList = []

        for threadPause in gcActivities.threadPauses:
            timeList.append(threadPause.time)
            threadPauseList.append(threadPause.threadPauseTime)
        return (timeList, threadPauseList)

    def getThreadAllPauseAndTime(self):
        timeList = []
        threadPauseList = []
        totalStoppedTime = 0

        for threadPause in gcActivities.threadPauses:
            timeList.append(threadPause.time)
            totalStoppedTime += threadPause.threadPauseTime
            threadPauseList.append(totalStoppedTime)
        return (timeList, threadPauseList)


def plotHeapUsage(appName, title, gcActivities):



    heapUsage = HeapUsage(gcActivities)

    fig, axes = plt.subplots(nrows=3, ncols=1, sharey=False, sharex=True, figsize=(6.3, 5))

    plt.rc('font', family='Helvetica', size=12)

    plt.subplots_adjust(left=0.11, bottom=0.12, right=0.96, top=0.92,
                        wspace=0.2, hspace=0.08)
    #gs = gridspec.GridSpec(3, 1)
    #axes[0] = plt.subplot(gs[0, :3])
    # identical to ax1 = plt.subplot(gs.new_subplotspec((0,0), colspan=3))
    #axes[1] = plt.subplot(gs[2:, :])


    axes[0].set_ylabel("Thread pause (ms)")
    axes[1].set_ylabel("Thread pause (ms)")
    axes[2].set_ylabel("GC pause (ms)")
    axes[2].set_xlabel("Time (s)")

    # axes[0].set_xlim(xmin=0)  # The ceil
    # axes[1].set_xlim(xmin=0)
    if (title == "Alexnet GC Metrics"):
        axes[2].set_xlim(0, 110)
    else:
        axes[2].set_xlim(0, 60)


    threadPauseAndTime = heapUsage.getThreadPauseAndTime()
    #if (len(gcPauseAndTime1) != 0):
    threadPause = axes[0].bar(threadPauseAndTime[0], threadPauseAndTime[1], 0.5, label='Suspended thread pause')

    allThreadPause = heapUsage.getThreadAllPauseAndTime()
    axes[1].plot(allThreadPause[0], allThreadPause[1], 'o-', linewidth=1.5, markersize=2, label='Accumulated thread pause')


    gcPauseAndTime1 = heapUsage.getGCPauseAndTime("Background partial concurrent mark sweep GC")
    #if (len(gcPauseAndTime1) != 0):
    partital = axes[2].bar(gcPauseAndTime1[0], gcPauseAndTime1[1], 0.5, label='Background partial CMS')

    gcPauseAndTime2 = heapUsage.getGCPauseAndTime("Background sticky concurrent mark sweep GC")
    #if (len(gcPauseAndTime2) != 0):
    if (title != "Alexnet GC Metrics"):
        strict = axes[2].bar(gcPauseAndTime2[0], gcPauseAndTime2[1], 0.3, label='Background sticky CMS')




    axes[0].legend(frameon=False)
    axes[1].legend(frameon=False)
    axes[2].legend(frameon=False)


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

    #print plt.rcParams['axes.prop_cycle'].by_key()['color']


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
