from os import system

BEFORE_TIME = 0.5
AFTER_TIME = 2
CSV_PATH = "./yeni_1.csv"
DOWNLOAD_PATH = "./videos2"
DATA_PATH = "./data2.csv"
VIDEO_URL = "https://www.youtube.com/watch?v=MFCSlbEDkHw"
VIDEO_OFFSET = 87.54

DOWNLOAD_VIDEO_CAP = 100

def hhmmssToSeconds(hhmmss: str) -> int:
    h, m, s = [int(a) for a in hhmmss.split(':')]
    return h*3600+m*60+s

def clearDataFile():
    try:
        system('rm data.txt')
        print("Data file removed")
    except:
        print("No data file")


DATA_FILE = open(DATA_PATH, 'a+')
def appendDataFile(line: str):
    DATA_FILE.write(line + "\n")

def main():
    data = open(CSV_PATH, 'r').read().split('\n')
    clearDataFile()

    templateString = f'yt-dlp -f "bestvideo/bestvideo" --external-downloader ffmpeg --external-downloader-args "ffmpeg_i:-ss %s -t {BEFORE_TIME + AFTER_TIME}" "{VIDEO_URL}" -o {DOWNLOAD_PATH}/%s.mp4'
    counter = 0
    for i, line in enumerate(data):
        if(i==0 or line == ""): continue #column names line or empty line
        values = line.split(',') 
        time, kmh, mph = values[1], values[11], values[46]
        if kmh == "0" or mph == "0": continue 

        startTime = hhmmssToSeconds(time) - BEFORE_TIME + VIDEO_OFFSET
        endTime = startTime + BEFORE_TIME + AFTER_TIME + VIDEO_OFFSET
        command = templateString % (startTime, counter)
        
        appendDataFile(f"./videos/{counter}.mp4,{mph},{kmh}")
        system(command)

        counter+=1
        if(counter >= DOWNLOAD_VIDEO_CAP and DOWNLOAD_VIDEO_CAP > 0):
            break

if __name__ == "__main__":
    main()