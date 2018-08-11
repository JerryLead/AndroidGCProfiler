from statistics.GCEvent import GCEvent
import time as Time


class GCActivities:
    # line = Background partial concurrent mark sweep GC freed 22037(4MB) AllocSpace objects, 9(79MB) LOS objects, 7% free, 190MB/206MB, paused 50.117ms total 712.383ms
    def parseGCEvent(self, line):
        timeStr = line[0: line.find(' ', line.find(' ') + 1)]
        #print(timeStr)
        time = Time.strptime(timeStr, "%m-%d %H:%M:%S.%f")
        gcCause = line[line.find('art:') + 5: line.find('freed') - 1]
        freedObjNum = int(line[line.find('freed') + 6: line.find('(')])
        freedObjSize = int(line[line.find('(') + 1: line.find('MB)')])
        largeObjNum = int(line[line.find(',') + 2: line.rfind('(')])
        largeObjSize = int(line[line.rfind('(') + 1: line.rfind('MB)')])
        used = int(line[line.rfind('free,') + 6: line.rfind('MB/')])
        allocated = int(line[line.rfind('/') + 1: line.rfind('MB')])
        gcPauseStr = line[line.rfind('paused') + 7: line.rfind(' total')]

        if(gcPauseStr.endswith('us')):
            gcPauseTime = float(gcPauseStr[0: gcPauseStr.rfind('us')])
            gcPauseTime = gcPauseTime / 1000
        elif(gcPauseStr.endswith('ms')):
            gcPauseTime = float(gcPauseStr[0: gcPauseStr.rfind('ms')])
        elif(gcPauseStr.endswith('s')):
            gcPauseTime = float(gcPauseStr[0: gcPauseStr.rfind('s')]) * 1000


        gcTotalStr = line[line.rfind(' ') + 1:]
        if(gcTotalStr.endswith('us')):
            gcTotalTime = float(gcTotalStr[0: gcTotalStr.rfind('us')])
            gcTotalTime = gcTotalTime / 1000
        elif(gcTotalStr.endswith('ms')):
            gcTotalTime = float(gcTotalStr[0: gcTotalStr.rfind('ms')])
        elif(gcTotalStr.endswith('s')):
            gcTotalTime = float(gcTotalStr[0: gcTotalStr.rfind('s')]) * 1000

        gcEvent = GCEvent(time, gcCause, freedObjNum, freedObjSize, largeObjNum, largeObjSize,
                          used, allocated, gcPauseTime, gcTotalTime)
        gcEvent.println()

    def parseThreadPause(self, line):
        timeStr = line[0: line.find(' ', line.find(' ') + 1)]
        #print(timeStr)
        time = Time.strptime(timeStr, "%m-%d %H:%M:%S.%f")

        pauseTotalStr = line[line.rfind(':') + 2:]
        if(pauseTotalStr.endswith('us')):
            pauseTotalTime = float(pauseTotalStr[0: pauseTotalStr.rfind('us')])
            pauseTotalTime = pauseTotalTime / 1000
        elif(pauseTotalStr.endswith('ms')):
            pauseTotalTime = float(pauseTotalStr[0: pauseTotalStr.rfind('ms')])
        elif(pauseTotalStr.endswith('s')):
            pauseTotalTime = float(pauseTotalStr[0: pauseTotalStr.rfind('s')]) * 1000

        print(str(time) + "|" + str(pauseTotalTime))


if __name__ == '__main__':


    gcActivities = GCActivities()
    line = "06-16 12:07:14.971 27469-27479/com.library.example.nin I/art: Background partial concurrent mark sweep GC freed 22037(4MB) AllocSpace objects, 9(79MB) LOS objects, " \
           "7% free, 190MB/206MB, paused 50.117ms total 712.383ms"
    threadPauseline = "06-16 12:07:18.646 27469-27479/com.library.example.nin W/art: Suspending all threads took: 7.230ms"

    gcActivities.parseGCEvent(line)
    gcActivities.parseThreadPause(threadPauseline)
