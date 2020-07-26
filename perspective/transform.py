# Importing necessary packages
import numpy as np
import cv2

def order_points(pts):
    # Initializing a list of co-ordinates of the image
    # in the order: 
    # top-left,
    # top-right,
    # bottom-right,
    # bottom-left
    rect = np.zeros((4,2), dtype="float32")

    # The top-left point will have minimu sum
    # while the bottom-right point will have the maximum
    s  = pts.sum(axis=1)
    rect[0] =  pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    # The top-right point will have the minimum difference
    # while, the bottom-left will have the maximum.
    d = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(d)]
    rect[3] = pts[np.argmax(d)]

    # Return the co-ordinates
    return rect


def four_pt_transform(image, pts):
    # Obtaining a consistent order of points and unpacking them
    rect = order_points(pts)
    (tl, tr, br, bl) =  rect

    # Computing the width of the new transformed image which will be maximum of
    # distance between top-left and top-right x-coordinate and,
    # distance between bottom-left and bottom-right x-coordinate
    widthA = np.sqrt(((br[0] - bl[0])**2) + ((br[1] - bl[1])**2 ))
    widthB = np.sqrt(((tr[0] - tl[0])**2) + ((tr[1] - tl[1])**2 ))
    maxWidth = max(int(widthA), int(widthB))
    
    # Computing the height similar to the above calcualtions
    heightA = np.sqrt(((br[0] - tr[0])**2) + ((br[1] - tr[1])**2 ))
    heightB = np.sqrt(((bl[0] - tl[0])**2) + ((bl[1] - tl[1])**2 ))
    maxHeight = max(int(heightA), int(heightB))

    # Constructing the set of destination points to obtain a top-down view of 
    # the image again specifying the points in the already mentioned order
    dst = np.array([
        [0,0],
        [maxWidth-1, 0],
        [maxWidth-1, maxHeight-1],
        [0, maxHeight-1]], dtype="float32")

    # Computing the perspective transform matrix and applying it
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

    # Returning the warped image
    return warped
