import math
from interfaces.IDistanceCalc import IDistanceCalc
class DistanceCalc(IDistanceCalc):
    def __init__(self):
        self.TENNIS_BALL_SIZE = 0.067

    def getPointInformation(self, pt: tuple[int, int, float], pixelSize: float, focalLength: float, resolution: tuple[int, int]) -> tuple[float, float, float]:
        ptxDeflectionPixels = pt[0] - resolution[0]/2
        ptxDeflection = ptxDeflectionPixels*pixelSize
        ptyDeflectionPixes = (pt[1] - resolution[1]/2) *(-1)
        ptyDeflection = ptyDeflectionPixes*pixelSize

        ptDeflection = (ptxDeflection**2 + ptyDeflection**2)**(1/2)

        ptDistanceInCamera = (focalLength**2 + ptDeflection**2)**(1/2)
        ptSize = pt[2]*2*pixelSize
        ptDistance = ptDistanceInCamera*self.TENNIS_BALL_SIZE/ptSize

        return ptxDeflection, ptyDeflection, ptDistance, ptDistanceInCamera

    def run(self, pt1: tuple[int, int, float], pt2: tuple[int, int, float], pixelsizemicron: float, focalLengthmm: float, resolution: tuple[int, int]) -> float:

        pixelSize = pixelsizemicron*1e-6
        focalLength = focalLengthmm*1e-3
        
        pt1xDeflection, pt1yDeflection, pt1Distance, pt1DistanceInCamera = self.getPointInformation(pt1, pixelSize, focalLength, resolution)
        pt2xDeflection, pt2yDeflection, pt2Distance, pt2DistanceInCamera = self.getPointInformation(pt2, pixelSize, focalLength, resolution)

        lineBetweenPoints = ((pt2xDeflection-pt1xDeflection)**2 + (pt2yDeflection-pt1yDeflection)**2)**(1/2)

        cosAlfa = (pt1DistanceInCamera**2 + pt2DistanceInCamera**2 - lineBetweenPoints**2) / (2*pt1DistanceInCamera*pt2DistanceInCamera)

        distance = (pt1Distance**2 + pt2Distance**2 - 2*pt1Distance*pt2Distance*cosAlfa)**(1/2)

        return distance

def main(): #3.81
    distanceCalc = DistanceCalc()
    pixelSize = 4.409722214
    focalLength = 120

    speed1 = distanceCalc.run((1708, 354, 7.5), (1878, 1508, 9), pixelSize, focalLength, (3840, 2160)) / 0.4 * 3.6
    speed2 = distanceCalc.run((2335, 354, 7.5), (1383, 1461, 9), pixelSize, focalLength, (3840, 2160)) / 0.44 * 3.6
    speed3 = distanceCalc.run((1518, 379, 7.5), (2472, 1463, 9), pixelSize, focalLength, (3840, 2160)) / 0.44 * 3.6
    speed4 = distanceCalc.run((2307, 412, 7.5), (1727, 1511, 9), pixelSize, focalLength, (3840, 2160)) / 0.4 * 3.6
    speed5 = distanceCalc.run((1728, 1153, 10), (2288, 981, 8.5), pixelSize, focalLength, (3840, 2160)) / 0.36 * 3.6

    speedReal = distanceCalc.run((1722, 357, 10), (1896, 1518, 13.0), pixelSize, focalLength, (3840, 2160)) / 0.4 * 3.6
    print(speedReal)

    print(f"189 -> {speed1:.2f} -> {abs(speed1-189)/189*100:.2f}%") # 189 km/h
    print(f"181 -> {speed2:.2f} -> {abs(speed2-181)/181*100:.2f}%") # 181 km/h
    print(f"170 -> {speed3:.2f} -> {abs(speed3-170)/170*100:.2f}%") # 170 km/h
    print(f"189 -> {speed4:.2f} -> {abs(speed4-189)/189*100:.2f}%") # 189 km/h
    print(f"164 -> {speed5:.2f} -> {abs(speed5-164)/164*100:.2f}%") # 164 km/h

if __name__ == "__main__":
    main()