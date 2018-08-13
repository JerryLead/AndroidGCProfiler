class GCEvent:
    def __init__(self, time, gcCause, freedObjNum, freedObjSize, largeObjNum, largeObjSize,
                 used, allocated, gcPauseTime, gcTotalTime):
        self.time = time
        self.gcCause = gcCause
        self.freedObjNum = freedObjNum
        self.freedObjSize = freedObjSize #MB
        self.largeObjNum = largeObjNum
        self.largeObjSize = largeObjSize #MB
        self.used = used #MB
        self.allocated = allocated #MB
        self.gcPauseTime = gcPauseTime #ms
        self.gcTotalTime = gcTotalTime #ms


        # refers to https://developer.android.com/studio/profile/investigate-ram
        if (gcCause.find("Explicit") != -1):
            self.gcReason = "Explicit"
        elif (gcCause.find("Background") != -1):
            self.gcReason = "Background"
        else:
            print ("Error in parsing the GC type !!!")

        self.gcName = "Concurrent mark sweep (CMS)"
        if (gcCause.find("partial mark sweep") != -1):
            self.gcName = "partial mark sweep"
        elif (gcCause.find("sticky mark sweep") != -1):
            self.gcName = "sticky mark sweep"


    # def getTime(self):
    #     return self.time
    #
    # def getGCCause(self):
    #     return self.gcCause
    #
    # def getFreedObjNum(self):
    #     return self.freedObjNum
    #
    # def getFreedObjSize(self):
    #     return self.freedObjSize
    #
    # def getLargeObjNum(self):
    #     return self.largeObjNum
    #
    # def getLargeObjSize(self):
    #     return self.largeObjSize
    #
    # def getUsed(self):
    #     return self.used
    #
    # def getAllocated(self):
    #     return self.allocated
    #
    # def getGCPauseTime(self):
    #     return self.gcPauseTime
    #
    # def getGCTotalTime(self):
    #     return self.gcTotalTime

    def println(self):
        print(str(self.time) + '|' + self.gcCause + '|' + str(self.freedObjNum) + '|'
              + str(self.freedObjSize) + 'MB|' + str(self.largeObjNum) + '|'
              + str(self.largeObjSize) + 'MB|' + str(self.used) + 'MB|' + str(self.allocated) + 'MB|'
              + str(self.gcPauseTime) + 'ms|' + str(self.gcTotalTime)) + 'ms'

