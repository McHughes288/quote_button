from picamera.array import PiRGBArray
from picamera import PiCamera
import datetime
import imutils
import json
import time
import cv2

class Camera:
    def __init__(
        self,
        pi,
        fps=16,
        resolution=[640, 480],
        camera_warmup_time=1,
        delta_thresh=5,
	    min_area=5000,
	    min_alert_seconds=8.0,
	    min_motion_frames=8,
        greeting_sound="/home/pi/mnt/gdrive/Brian/17.wav",
        save_image=True,
        save_image_location="/home/pi/mnt/gdrive/images",
    ):

        self.pi = pi
        self.camera_warmup_time = camera_warmup_time
        self.delta_thresh = delta_thresh
        self.min_area = min_area
        self.min_alert_seconds = min_alert_seconds
        self.min_motion_frames = min_motion_frames
        self.greeting_sound = greeting_sound
        self.save_image = save_image
        self.save_image_location = save_image_location

        # initialize the camera and reference to the raw camera capture
        self.camera = PiCamera()
        self.camera.resolution = tuple(resolution)
        self.camera.framerate = fps
        self.rawCapture = PiRGBArray(self.camera, size=tuple(resolution))

        # initialize detection variables
        self.reset_detection()

    def reset_detection(self):
        self.avg = None
        self.last_detected = datetime.datetime.now()
        self.motionCounter = 0

    def get_diff_to_average(self, frame):
        # resize the frame, convert it to grayscale, and blur it
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        
        # if the average frame is None, initialize it
        if self.avg is None:
            print("[CAMERA] starting background model...")
            self.avg = gray.copy().astype("float")

        # accumulate the weighted average and compute the difference
        cv2.accumulateWeighted(gray, self.avg, 0.5)
        frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(self.avg))

        return frameDelta

    def get_contours_from_delta(self, frameDelta):
        
        # threshold the delta, dilate to fill in gaps and find contours
        thresh = cv2.threshold(frameDelta, self.delta_thresh, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        return cnts

    def infer_motion(self, cnts):
        motion_detected = False
        for c in cnts:
            if cv2.contourArea(c) > self.min_area:
                motion_detected = True    
        return motion_detected
       
    def customise_frame(self, frame, cnts, timestamp):
        # compute the bounding box for the contour
        for c in cnts:
            # if the contour is too small, ignore it
            if cv2.contourArea(c) < self.min_area:
                continue
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # draw the text and timestamp on the frame
        long_ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
        cv2.putText(
            frame,
            "Motion detected, bello there sir",
            (10, 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 0, 255),
            2,
        )
        cv2.putText(
            frame,
            long_ts,
            (10, frame.shape[0] - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.35,
            (0, 0, 255),
            1,
        )
        return frame

    def save_frame(self, frame, timestamp):
        if self.save_image:
            short_ts = timestamp.strftime("%Y%m%dT%H%M%S")
            image_path = f"{self.save_image_location}/{short_ts}.jpg"
            cv2.imwrite(image_path, frame)

    def decide_to_greet_person(self, motion_detected, timestamp, frame):
        # play sound and save image if time between detections is large enough 
        # and there is consistent motion
        greet = False
        if motion_detected:
            if (timestamp - self.last_detected).seconds >= self.min_alert_seconds:
                self.motionCounter += 1
                if self.motionCounter >= self.min_motion_frames:
                    print("[CAMERA] Greeting user and saving frame...")
                    greet = True
                    self.save_frame(frame, timestamp)
                    # update timestamp and reset the motion counter
                    self.last_detected = timestamp
                    self.motionCounter = 0
        else:
            self.motionCounter = 0
        return greet

    def detect_motion(self, f):
        timestamp = datetime.datetime.now()
        
        frame = imutils.resize(f.array, width=500)
        frameDelta = self.get_diff_to_average(frame)
        contours = self.get_contours_from_delta(frameDelta)
        frame = self.customise_frame(frame, contours, timestamp)

        motion_detected = self.infer_motion(contours)
        greet = self.decide_to_greet_person(motion_detected, timestamp, frame)
        return greet

    def start_camera(self):
        print("[CAMERA] Camera warming up...")
        time.sleep(self.camera_warmup_time)

        # capture frames from the camera
        for f in self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True):
            self.rawCapture.truncate(0)
            motion = self.detect_motion(f)
            if motion:
                self.pi.play_sound(self.greeting_sound)
            
            



