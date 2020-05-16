import cv2
import imutils
import numpy as np
from sklearn.metrics import pairwise
import mss, os

background = None 
_cnt = 0

dir_path = os.getcwd()
print(dir_path)
full_path = dir_path + '\screenshots'
if not os.path.exists(full_path):
    os.makedirs(full_path)
print(full_path)    

def compute_running_average(image, avgWeight):
	global background
	if background is None:
		background = image.copy().astype("float")
		return
	cv2.accumulateWeighted(image, background, avgWeight)


def segmentation(image, threshold=25):
	global background

	diff = cv2.absdiff(background.astype("uint8"), image) 
    #print(diff)

	thresholded = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)[1] 
    #print(thresholded)

	(_, cnts, _) = cv2.findContours(thresholded.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 
    #print(cnt)

	if len(cnts) == 0:
		return
	else:
		segmented = max(cnts, key = cv2.contourArea)
		return (thresholded, segmented)


def count_fingers(thresholded, segmented):

    conver_hull = cv2.convexHull(segmented)
    
    extreme_top = tuple(convex_hull[convex_hull[:, :, 1].argmin()][0]) 
    extreme_bottom = tuple(convex_hull[convex_hull[:, :, 1].argmax()][0])
    extreme_left = tuple(convex_hull[convex_hull[:, :, 0].argmin()][0])
    extreme_right = tuple(convex_hull[convex_hull[:, :, 0].argmax()][0])
    #print(extreme_top + " " + extreme_bottom + " " + extreme_left + " " + extreme_right)

    cX = (extreme_left[0] + extreme_right[0]) / 2
    cY = (extreme_top[1] + extreme_bottom[1]) / 2
    cX = np.round(cX).astype("int") #convert to int
    cY = np.round(cY).astype("int")

    distance = pairwise.euclidean_distances([(cX, cY)], Y=[extreme_left, extreme_right, extreme_top, extreme_bottom])[0]
    maximum_distance = distance[distance.argmax()]
    #print(maximum_distance)

    radius = int(0.8 * maximum_distance)
    
    circumference = (2 * np.pi * radius)

    circular_roi = np.zeros(thresholded.shape[:2], dtype="uint8")
    print(circular_roi)
    circulat_roi = np.round(circular_roi).astype("int")
    
    cv2.circle(circular_roi, (cX, cY), radius, 255, 1)
    
    circular_roi = cv2.bitwise_and(thresholded, thresholded, mask=circular_roi)

    (_, cnts, _) = cv2.findContours(circular_roi.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    count = 0

    for c in cnts:

        (x, y, w, h) = cv2.boundingRect(c)

        if ((cY + (cY * 0.25)) > (y + h)) and ((circumference * 0.25) > c.shape[0]):
            count += 1
    return count

def captureScreen(fingers):
    global _cnt
    with mss.mss() as sct:
        filename = sct.shot(mon = -1, output = full_path + '\screenshot_{}.png'.format(str(_cnt)))
        print(filename)
        _cnt = _cnt + 1
        
def compute():

    alphaWeight = 0.5 
    stream = 'http://192.168.0.4:8080/video'

    camera = cv2.VideoCapture(stream)

    top, right, bottom, left = 10, 350, 225, 590
    
    num_frames = 0 

    while True:
        (_, frame) = camera.read()

        frame = imutils.resize(frame, width=700) 
        frame = cv2.flip(frame, 1) 
        clone = frame.copy()    

        (height, width) = frame.shape[:2]
        #print(str(height) +" "+ str(width))

        roi = frame[top:bottom, right:left] 

        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (7,7), 0) 

        if num_frames < 30:
            compute_running_average(gray, alphaWeight)
        else:
            hand = segmentation(gray)

            if hand is not None:
                (thresholded, segmented) = hand
                #print(thresholded)
                #print(segmented)
                cv2.drawContours(clone, [segmented + (right, top)], -1, (0, 0, 255)) #(destination_img, contours to draw, contourIdx(-1 denotes all contours are drawn), color)
                
                fingers = count_fingers(thresholded, segmented)
                    
                cv2.putText(clone, "Detected Value: "+str(fingers), (70,45), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0 , 255), 2)

                cv2.imshow("Thresholded", thresholded)
                captureScreen(fingers)
                
        cv2.rectangle(clone, (left, top), (right,bottom), (0, 255, 0), 2)
        num_frames +=1
        cv2.imshow("Output", clone)
        keypress = cv2.waitKey(1) & 0xFF
        if keypress == ord("q"):
            break
    
    camera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    compute()
