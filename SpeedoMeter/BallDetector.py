import os
import torch

from models.yolo import Model
from models.common import Detections
from utils.torch_utils import select_device

from interfaces.IBallDetector import IBallDetector

class BallDetector(IBallDetector):
    def __init__(self):
        self._loadModel()

    def _loadModel(self):
        path = os.path.join(os.path.dirname(__file__), 'weights/best.pt')
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        stateDict = torch.load(path, map_location=device)
        stateDictModel = stateDict['model']

        self.model = Model(stateDictModel.yaml).to(next(stateDictModel.parameters()).device)
        self.model.load_state_dict(stateDictModel.float().state_dict())
        self.model.names = stateDictModel.names
        self.model = self.model.autoshape()

    def clearResult(self, result: Detections):
        def avg(num1, num2): return (num1+num2)/2
        detections = list()
        for position in result.xyxy[0]:
            detections.append([
                int(avg(position[0], position[2])), 
                int(avg(position[1], position[3])), 
                (position[2]-position[0])/2
            ])
        return detections


    def run(self, image):
        result = self.model(image)

        return self.clearResult(result)

        