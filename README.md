# 2017BTECS00016_2017BTECS00061_2017BTECS00099
# The hand gestures are to be recognized to build an application. Given images of hand gestures, implement suitable segmentation algorithm to detect hand .

Steps:
Segment hand region from a real-time video sequence

Background Subtraction
Motion Detection and Thresholding
Contour Extraction
Count fingers

Get convex hull of the segmented hand region and compute the most extreme points in the convex hull
Get center of palm using extremes points
Using center of palm, construct a circle with the maximum Euclidean distance as radius
Perform bitwise AND operation on thresholded hand image and the circular ROI
Compute count of fingers using the finger slices obtained in previous step

# To run the file use: python sudo.py

 Memory Intensive Operation
 This script creates screenshot for every frame captured and stores it in directory 'screenshots'
 Hence, there is a little delay during frame capture

# TO-DO List
 Segment hand region
 Detect numbers using count of fingers
 
# Project by: Harshit Jaiswal 2017BTECS00016 Akash Kore 2017BTECS00061 Komal Jadhav 2017BTECS00099
