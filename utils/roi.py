def get_bed_roi(frame, roi_width=1000):
    h, w = frame.shape[:2]
    x1 = w//2 - roi_width//2
    x2 = w//2 + roi_width//2
    return frame[:, x1:x2], (x1, x2)
