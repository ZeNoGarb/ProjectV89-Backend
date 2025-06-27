import cv2
import numpy as np
from .roi import get_bed_roi

def preprocess(frame):
    roi, _ = get_bed_roi(frame)
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    return gray

def detect_motion_score(prev_gray, frame, threshold=50):
    roi, _ = get_bed_roi(frame)
    curr_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    curr_gray = cv2.GaussianBlur(curr_gray, (5, 5), 0)

    diff = cv2.absdiff(prev_gray, curr_gray)
    _, mask = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))

    motion_score = np.sum(mask) / 255
    return motion_score, mask, roi, curr_gray
