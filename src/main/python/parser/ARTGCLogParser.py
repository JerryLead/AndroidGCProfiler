from reader import FileReader
from statistics.GCActivities import GCActivities

if __name__ == '__main__':

    gcLogPath = "/Users/xulijie/Documents/GCResearch/Android/logs/"
    gcFileName = "cnndroid_alexnet_scale1_image_time_logcat.txt"


    gcLines = FileReader.readLines(gcLogPath + gcFileName)
    gcActivities = GCActivities(gcLines)


    line = "06-16 12:07:14.971 27469-27479/com.library.example.nin I/art: Background partial concurrent mark sweep GC freed 22037(4MB) AllocSpace objects, 9(79MB) LOS objects, " \
           "7% free, 190MB/206MB, paused 50.117ms total 712.383ms"
    threadPauseline = "06-16 12:07:18.646 27469-27479/com.library.example.nin W/art: Suspending all threads took: 7.230ms"

    gcActivities.parseGCEvent(line)
    gcActivities.parseThreadPause(threadPauseline)