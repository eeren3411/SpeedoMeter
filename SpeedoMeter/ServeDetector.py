import cv2 as cv
import numpy as np
from interfaces.IServeDetector import IServeDetector
#import openpose.pyopenpose as op

class ServeDetector(IServeDetector):
    def __init__(self):
        self.BODY_PARTS = { "Nose": 0, "Neck": 1, "RShoulder": 2, "RElbow": 3, "RWrist": 4,
                            "LShoulder": 5, "LElbow": 6, "LWrist": 7, "RHip": 8, "RKnee": 9,
                            "RAnkle": 10, "LHip": 11, "LKnee": 12, "LAnkle": 13, "REye": 14,
                            "LEye": 15, "REar": 16, "LEar": 17, "Background": 18 }
        
        #self.net = cv.dnn.readNetFromTensorflow("graph_opt.pb")

    def _cropImage(self, image, leftPercantage, rightPercantage, topPercantage, bottomPercantage):
        height = image.shape[0]
        width = image.shape[1]
        print(leftPercantage/100*width, (100-rightPercantage)/100*width, topPercantage/100*height, (100-bottomPercantage)/100*height)
        return image[int(topPercantage/100*height) : int((100-bottomPercantage)/100*height), int(leftPercantage/100*width) : int((100-rightPercantage)/100*width)]

    def run(self, video):
        return 7
        threshold = 0.2
        flag, frame = video.read()
        frame = self._cropImage(frame, 15, 15, 17, 0)
        cv.imwrite("test.png", frame)

        params = {"model_folder": "./openposeModels"}
        openpose = op.OpenPose(params)

        datum = op.Datum()
        datum.cvInputData = frame
        openpose.emplaceAndPop([datum])

        keyPoints = list()
        for i in range(datum.poseKeypoints.shape[0]):
            handKeyPoints = datum.handKeypoints[i]
            leftHand = handKeyPoints[0, :, :]
            rightHand = handKeyPoints[1, :, :]
            nose = datum.poseKeypoints[i, 0, :2]
            keyPoints.append((nose, leftHand, rightHand))

        print(keyPoints)


if __name__ == "__main__":
    video = cv.VideoCapture('./0.mp4')
    print(video.get(3)) # width
    print(video.get(4)) # height
    print(video.get(5)) # fps
    serveDetector = ServeDetector()
    serveDetector.run(video)