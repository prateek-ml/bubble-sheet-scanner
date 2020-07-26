# Importing the necessary packages
from perspective.transform import four_pt_transform
import numpy as np
import argparse
import imutils
from imutils import contours
import cv2

#Constructing the argument parser and parsing the arguments
ap = argparse.ArgumentParser()
#ap.add_argument('-i', '--image', required=True, help='Path to the input image')
args = vars(ap.parse_args())

#Defining the answer key which maps the question number to correct answer for our sample image
ANSWER_KEY = {0:1, 1:4, 2:0, 3:3, 4:1}


#Loading the image, converting into grayscale and blurring it to find edges
image = cv2.imread('images/test_02.png')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5,5), 0)
edged = cv2.Canny(blurred, 75, 200)

#Finding contours in the edge map, then initializing the contours corresponding to the document
conts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
conts = imutils.grab_contours(conts)
docCont = None

#Ensuring atleast 1 contour is found
if len(conts) >0:
    #Sorting the contours according to their size in descending order
    conts = sorted(conts, key=cv2.contourArea, reverse=True)

    #Looping over the sorted contours
    for c in conts:
        #approximating the contours
        pm = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02*pm, True)

        #If approximated contour has 4 points, it is the document
        if len(approx) == 4:
            docCont = approx
            break

# Applying 4-point transform to both original and grayscale image to obtain a top-down view of the paper
paper = four_pt_transform(image, docCont.reshape(4,2))
warped = four_pt_transform(gray, docCont.reshape(4,2))

#Applying thresholding to binarize the warped piece of paper
thresh = cv2.threshold(warped, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

# Now we will find the contours in the threshold image corresponding to the questions
conts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
conts = imutils.grab_contours(conts)
questions = []

#Looping over the contours
for c in conts:
    #Computing the bounding box of the contour and using it to derive the aspect ratio
    (x,y,w,h) = cv2.boundingRect(c)
    ar = w/float(h)

    #To label the contour as question, the region should be sufficiently wide and tall, and an aspect ratio approxiamtely 1
    if w>=20 and h>=20 and ar>=0.8 and ar<=1.1:
        questions.append(c)

#Sorting the question contours top-to-bottom
questions = contours.sort_contours(questions, method='top-to-bottom')[0]
correct = 0

#Each question has 5 possible answers, looping over questions in batches of 5
for (q,i) in enumerate(np.arange(0, len(questions), 5)):
    #Sorting the contours from left to right for the current question
    conts = contours.sort_contours(questions[i:i+5])[0]
    bubbled = None
    
    #Looping over sorted contours
    for (j,c) in enumerate(conts):
        #Constructing a mask to reveal the current bubble for question
        mask = np.zeros(thresh.shape,dtype="uint8")
        cv2.drawContours(mask, [c], -1, 255, -1)

        #Applying mask to threshold image and counting number of non-zero pixels in bubble area
        mask = cv2.bitwise_and(thresh, thresh, mask=mask)
        total = cv2.countNonZero(mask)

        #If current total has larger number of non-zero pixels, we are currently examining bubbled-in answer
        if bubbled is None or total > bubbled[0]:
            bubbled = (total, j)   

    #Initializing the contour color and the index of the correct answer
    color = (0,0,255)
    k = ANSWER_KEY[q]

    #Checking if the bubbled answer is correct
    if k == bubbled[1]:
        color = (0,255,0)
        correct += 1
    #Drawing the outline of the correct answer 
    cv2.drawContours(paper, [conts[k]], -1, color, 3)


#Calculating scores
score = (correct/5.0) *100
print("[INFO] score: {:.2f}%".format(score))
cv2.putText(paper, "{:.2f}%".format(score), (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,0,0), 2)
cv2.imshow("Original", image)
cv2.imshow("Exam", paper)
cv2.waitKey(0)
cv2.destroyAllWindows()