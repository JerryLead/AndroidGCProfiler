class GCEvent:
    def __init__(self, time, threadPauseTime):
        self.time = time
        self.threadPauseTime = threadPauseTime

    def getTime(self):
        return self.time

    def getThreadPauseTime(self):
        return self.threadPauseTime

    def println(self):
        print(str(self.time) + '|' + self.threadPauseTime + 'ms')

