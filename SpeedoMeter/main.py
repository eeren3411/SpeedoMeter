from SpeedoMeter import SpeedoMeter
from ApiDetector import ApiDetector
import os

VIDEOS_FOLDER_PATH = "./croppedVideos/"
OUTPUT_FILE_PATH = "./results.txt"

def main():
    speedoMeter = SpeedoMeter(BallDetector=ApiDetector)

    files = [VIDEOS_FOLDER_PATH + file for file in os.listdir(VIDEOS_FOLDER_PATH) if os.path.isfile(VIDEOS_FOLDER_PATH + file)]
    outputFile = open(OUTPUT_FILE_PATH, 'w+')

    for file in files:
        result = None
        try:
            result = speedoMeter.run(file)
        except Exception as e:
            result = e
        outputFile.write(file + "\t" + str(result) + "\n")

    """
    result = speedoMeter.run('./croppedVideos/3.mp4')
    print(result)
    """

def test():
    fileName = '15.mp4'
    speedoMeter = SpeedoMeter(BallDetector=ApiDetector)
    result = speedoMeter.run('./croppedVideos/' + fileName)
    print(fileName + " -> " + str(result))

if __name__ == "__main__":
    test()