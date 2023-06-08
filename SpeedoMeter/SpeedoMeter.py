import cv2 as cv
import math
from interfaces.IBallDetector import IBallDetector
from interfaces.ICameraInformation import ICameraInformation
from interfaces.IServeDetector import IServeDetector
from interfaces.IDistanceCalc import IDistanceCalc

class SpeedoMeter:
    def __init__(
            self, 
            BallDetector = None, 
            CameraInformation = None, 
            ServeDetector = None,
            DistanceCalc = None
    ):
        if BallDetector == None:
            from BallDetector import BallDetector
            self.BallDetector = BallDetector
        else:
            self.BallDetector = BallDetector
        
        if CameraInformation == None:
            from CameraInformation import CameraInformation
            self.CameraInformation = CameraInformation
        else:
            self.CameraInformation = CameraInformation
        
        if ServeDetector == None:
            from ServeDetector import ServeDetector
            self.ServeDetector = ServeDetector
        else:
            self.ServeDetector = ServeDetector

        if DistanceCalc == None:
            from DistanceCalc import DistanceCalc
            self.DistanceCalc = DistanceCalc
        else:
            self.DistanceCalc = DistanceCalc
        

    def run(self, video, threshold = 0.45, hardThreshold = 0.32):
        cameraInformation = self.CameraInformation()
        serveDetector = self.ServeDetector()
        ballDetector = self.BallDetector()
        distanceCalc = self.DistanceCalc()

        if type(video) == type("str"):
            video = cv.VideoCapture(video)
        
        width = video.get(3)
        height = video.get(4)
        fps = video.get(5)

        pixelSize, focalLength = cameraInformation.run(video)
        
        video.set(cv.CAP_PROP_POS_FRAMES, 0)
        serveFrame = serveDetector.run(video)
    
        serveFramesToSearch = (
            list(range(serveFrame, serveFrame + 2, 1)) +
            list(range(serveFrame - 1, serveFrame - 3, -1))
        )

        bestServeFrame = None
        bestServeFrameId = None
        bestServePoint = None

        print("Searching for ball at serve")
        for tempServeFrameId in serveFramesToSearch:
            video.set(cv.CAP_PROP_POS_FRAMES, tempServeFrameId)
            flag, tempFrame = video.read()
            if not flag:
                print("Serve frame could not be found")
                raise ValueError("Serve frame could not be found")
            
            flag, tempPoint = ballDetector.run(tempFrame)
            
            if not flag: continue

            print(tempServeFrameId, tempPoint[3])

            if bestServePoint == None or bestServePoint[3] < tempPoint[3]:
                bestServePoint = tempPoint
                bestServeFrameId = tempServeFrameId
                bestServeFrame = tempFrame

            if bestServePoint != None and bestServePoint[3] > threshold:
                break

        if bestServePoint == None or bestServePoint[3] < hardThreshold:
            print("Ball could not be found at serve")
            raise ValueError("Ball could not be found at serve")

        """
        video.set(cv.CAP_PROP_POS_FRAMES, serveFrame)
        flag, frame = video.read()
        
        if not flag:
            print("Frames could not be extracted")
            raise ValueError()

        flag, firstPoint = ballDetector.run(frame)
        """

        outframe = cv.circle(bestServeFrame, (int(bestServePoint[0]), int(bestServePoint[1])), int(bestServePoint[2]), (255, 255, 255), 3)
        cv.imwrite('firstFrame%s.jpg' % bestServeFrameId, outframe)

        # .4 seconds is great place to start searching for ball again
        searchFrame = serveFrame + int(0.4*fps)

        framesToSearch = (
            list(range(searchFrame, searchFrame + 3, 1)) + 
            list(range(searchFrame - 1, searchFrame - 4, -1)) + 
            list(range(searchFrame + 3, searchFrame + 6, 1)) + 
            list(range(searchFrame - 4, searchFrame - 7, -1))
        )
        
        bestSecondFrame = None
        bestSecondFrameId = None
        bestSecondPoint = None
        print("Searching ball at a second frame")
        for frameId in framesToSearch:
            video.set(cv.CAP_PROP_POS_FRAMES, frameId)
            flag, tempFrame = video.read()
            if not flag:
                print("Second frame could not be found")
                raise ValueError("Second frame could not be found")

            flag, tempPoint = ballDetector.run(tempFrame)
            
            if not flag: continue

            print(frameId, tempPoint[3])

            if bestSecondPoint == None or bestSecondPoint[3] < tempPoint[3]:
                bestSecondPoint = tempPoint
                bestSecondFrame = tempFrame
                bestSecondFrameId = frameId
            
            if bestSecondPoint != None and bestSecondPoint[3] > threshold:
                break
        
        if bestSecondPoint == None or bestSecondPoint[3] < hardThreshold:
            print("Ball could not be found in spesific time limit")
            raise ValueError("Ball could not be found in spesific time limit")

        print(bestSecondFrameId, bestSecondPoint[3])
        bestSecondFrame = cv.circle(bestSecondFrame, (bestSecondPoint[0], bestSecondPoint[1]), int(bestSecondPoint[2]), (255, 255, 255), 3)
        cv.imwrite('secondFrame%s.jpg' % bestSecondFrameId, bestSecondFrame)
        
        distance = distanceCalc.run(
            pt1 = bestServePoint,
            pt2 = bestSecondPoint,
            pixelsizemicron = pixelSize,
            focalLengthmm = focalLength,
            resolution = (width, height)
        )

        timeDelta = (bestSecondFrameId - bestServeFrameId) / fps
        mps = distance / timeDelta
        kmh = mps*3.6
        return kmh
    

if __name__ == "__main__":
    video = cv.VideoCapture("1.mp4")
    flag, frame = video.read()
    cv.imshow("firstFrame", frame)
    cv.waitKey(0)

    video.set(cv.CAP_PROP_POS_FRAMES, 20)
    flag, frame = video.read()
    cv.imshow("secondFrame", frame)
    cv.waitKey(0)