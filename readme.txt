Theory:
Get images binary thresholded after grayscale conversion, next transform it to cluster closeby transition spaces in image(Image Morphology used, results were better than dialation erotion), find contours, filter contours, draw bounding box, save video, save csv.

To run:
1. go to terminal
2. install requirements.txt
3. python3 car_tracking.py
Note: Console logs - Bounding box names and parameters used to threshold. This can be used for further improvement of threshold values.


Additional Info:
The function named filter_contours currently uses aspect ratio and contour area to filter contours, there are lot of experiments is to be done to finetune te outcomes.
In settings dictionary(line no 12) those experimental values can be provided.

Output:
Output folders contains a csv and video file.
Each row in csv has a unique key which is the frame no, the value for the same is a list of dictionary containing contour no as key and box position(x,y,w,h) as value.
The video file is saved in 30 fps, feel free to play around with the fps in settings mentioned above.

Improvements:
lot of experiment can be done, inclution of new setting parameters like range of (w,h), contour shape estimation etc can be done to filter and get more accurate results. Subject to experiment.
Morphological operations can be tried alternatively, I tried dialation and erosion but morphology results were far better when comes to filling the gaps betwen closely associated contours. Might be subject to this problem statement, experiments can be done to find better algorithm to fill those gaps in closeby contours.

Feel free to contact me on any doubts regarding to the codes.
