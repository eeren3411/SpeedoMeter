# Our Project: High-Fidelity Ground-Truth Data Generation 

## Introduction
In our pursuit to generate reliable ground-truth data, we've utilized a database meticulously created using Hawk-Eye datasets. Our Python program cuts and downloads the relevant videos, forming the cornerstone of our process.

## Camera Information
The matches were broadcasted using a Sony 3500S camera. Understanding the technical specifications of this camera was essential for achieving high-fidelity results. We've experimented with different focal lengths within the range of 70mm-400mm, and found the best results with a guess of 120mm.

## Infrastructure
Our system is built around a configurable-class functions approach, utilizing a facade design pattern. This allows for interchanging the algorithms used within our projects based on project-specific requirements.

## Pose Estimation
Our infrastructure handles pose estimation, specifically in detecting serves and identifying the first frame. To obtain this pose data, we're using a combination of OpenPose and OpenCV 4.6.

## Object Detection
As part of our object detection process, we employ two different algorithms - a local AI model for detecting the ball and an online service developed explicitly for this task.

## Image Cropping
We've integrated a cropping algorithm that trims 20% from both sides of each frame, effectively reducing the total area to be processed. This significantly improves the overall speed of our pipeline.

## Distance Calculation
Our final step in the process involves a distance calculator class, tasked with calculating the distance between any two given points, using the principles of optics, particularly the known focal length and pixel size.

## Camera Setting Getter Class
We have a camera setting getter class that retrieves vital camera information such as pixel size and focal length. It is crucial for customizing the inputs of our program and adapting our infrastructure to smartphone devices.

## Distance Calculation Algorithm
Our custom-written distance calculation algorithm is based on the camera's pinhole principle. It involves several steps, including conversion of sensor size and focal length to meters, use of triangle similarity and Pythagorean theorem, and calculation of the real distance between the camera pinhole and the ball. 

![image](https://github.com/eeren3411/SpeedoMeter/assets/77689346/9300e12f-ca04-4a5b-b0ad-bb9bc72d3b5f)


For each mini-step, we use the Pythagorean theorem to calculate the actual distance. 

![image](https://github.com/eeren3411/SpeedoMeter/assets/77689346/f35cc3f4-3629-4feb-8fb7-f1485ca1cdd1)

We calculate the angle between two points using the cosine theorem. 

![image](https://github.com/eeren3411/SpeedoMeter/assets/77689346/4339da15-913f-4d58-8e2a-7b7169f944e4)

Using the reverse cosine formula, we calculate the cosine between two vectors, which is then used to calculate the actual distance between two points in the real world.

## Conclusion
Our carefully engineered infrastructure prioritizes flexibility and accuracy. The incorporation of a facade design pattern with configurable-class functions offers the unique advantage of algorithm interchangeability. We've implemented pose estimation, dual-object detection algorithms, a crop algorithm, and a distance calculator class. Each of these plays a pivotal role in our system, making it robust and efficient. Our system is adaptable, with potential for future implementation on diverse platforms, including smartphones.
