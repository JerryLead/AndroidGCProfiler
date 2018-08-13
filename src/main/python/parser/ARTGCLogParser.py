from reader import FileReader
from statistics.GCActivities import GCActivities

if __name__ == '__main__':

    gcLogPath = "/Users/xulijie/Documents/GCResearch/Android/logs/"
    gcFileName = "cnndroid_alexnet_scale1_image_time_logcat.txt"

    gcLines = FileReader.readLines(gcLogPath + gcFileName)
    gcActivities = GCActivities(gcLines)

    gcActivities.plotMemoryUsage()
