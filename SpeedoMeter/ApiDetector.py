from roboflow import Roboflow
import cv2
import sys

from interfaces.IBallDetector import IBallDetector

class ApiDetector(IBallDetector):
    def __init__(self):
        realStdOut = sys.stdout
        sys.stdout = open('trash', 'w')
        self._loadModel()
        sys.stdout = realStdOut

    def _loadModel(self):
        rf = Roboflow(api_key="YourApiKeyHere")
        project = rf.workspace().project("tennis-uc2es")
        self.model = project.version(1).model

    def clearResults(self, predictionJson):
        iWidth, iHeight = predictionJson['image'].values()
        sideThreshold = 20

        leftThreshold = int(iWidth)*sideThreshold/100
        rightThreshold = int(iWidth)*(100-sideThreshold)/100

        finalPredictions = list()

        for prediction in predictionJson['predictions']:
            centerX = prediction['width']/2 + prediction['x']
            centerY = prediction['height']/2 + prediction['y']
            radius = (prediction['width'] + prediction['height'])/4
            #radius = min(prediction['width'], prediction['height'])/2
            if( leftThreshold < centerX < rightThreshold):
                finalPredictions.append((int(centerX), int(centerY), radius, prediction['confidence']))
                break
        
        if len(finalPredictions) > 0:
            return True, finalPredictions[0]
        else:
            return False, None

    def run(self, image):
        cv2.imwrite('temp.jpg', image)
        predictions = self.model.predict('temp.jpg', confidence=1)
        predictions_json = predictions.json()

        return self.clearResults(predictions_json)

if __name__ == "__main__":
    apiDetector = ApiDetector()

    cap = cv2.VideoCapture('./1.mp4')
    cap.set(cv2.CAP_PROP_POS_FRAMES, 34)
    res, frame = cap.read()
    if res:
        result = apiDetector.run(frame)
        print(result)
        frame = cv2.circle(frame, (int(result[0]), int(result[1])), int(result[2]), (255, 255, 255), 3)
        cv2.imwrite('frame.jpg', frame)

        cv2.waitKey(0)