# Gesture_volume_control
The main objective of the <b>"Gesture_volume_control"</b>  project is automation.<br>
This is a computer vision project that automatically  adjusts the speaker volume using hand gestures.<br>
MediaPipe is a cross-platform framework for building multimodal applied machine learning models using the data avaliable in audio and video format.<br>
The model detects and tracks all the fingers by using the <b>"hand_tracking.py"</b>,and the code in this file is written in modular format so that it can be used anywhere by just calling it.<br>
In a single hand the above code can detect and track 21 points.<br>
<image src="images/hand_landmarks.png" width=500><br> 
Here in this project we are intersted in finding the poistion of "Thumb" and the "Index" finger.<br>
All the locations of the fingers are stored in an array.By indexing the position of 4 and 8 we can locate the position of "Thumb" and the "Index" finger.<br>
Then we find the distance between the fingers by using the formula ((x2-x1)^2+(y2-y1)^2)^(0.5).<br>
The "Pycaw" library has a method called <b>"volume.SetMasterVolumeLevel()"</b> by which, we can adjust the computer's speaker volume<br>
We find the minimum and maximum range of the volume and then we map the distance value with minimum and maximum range of the volume<br>
Then depending upon the distance, the speaker volume is adjusted.
## Output image when volume is high 
<image src="images/volume_high.jpeg" width=500><br> 
## Output image when volume is low 
<image src="images/volume_low.jpeg" width=500><br> 


