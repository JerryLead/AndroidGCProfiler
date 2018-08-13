
import datetime as datetime

class ThreadPause:
    def __init__(self, time, threadPauseTime):
        self.time = time
        self.threadPauseTime = threadPauseTime

    def getTime(self):
        return self.time

    def getThreadPauseTime(self):
        return self.threadPauseTime

    def println(self):
        print(str(self.time) + '|' + self.threadPauseTime + 'ms')


if __name__ == '__main__':
    timeStr1 = "06-16 13:37:01.861"
    timeStr2 = "06-16 14:37:08.814"
    time1 = datetime.datetime.strptime(timeStr1, "%m-%d %H:%M:%S.%f")
    time2 = datetime.datetime.strptime(timeStr2, "%m-%d %H:%M:%S.%f")
    t = time2 - time1
    print("time = " + str(t))
    print("time = " + str(t.total_seconds()))