# import the necessary packages
from scipy.spatial import distance as dist # 유클리디안 공식을 통한 거리 측정
from imutils.video import VideoStream # Pi camera 접근 허용(성능 좋음)
from imutils import face_utils
from threading import Thread
import numpy as np
# import playsound # for windows
import datetime
import argparse
import imutils
import time
import dlib
import cv2

# make alarm to wake the driver
def sound_alarm(path):
    # play an alarm sound
    # maybe we can use pygame.
    pass

def eye_aspect_ratio(eye):
	# compute the euclidean distances between the two sets of
	# vertical eye landmarks (x, y)-coordinates

    # 눈을 기준으로 왼쪽 끝이 0번 index고, 시계 방향으로 회전하면서 증가

    A = dist.euclidean(eye[1],eye[5])
    B = dist.euclidean(eye[2],eye[4])

	# compute the euclidean distance between the horizontal
	# eye landmark (x, y)-coordinates
    C = dist.euclidean(eye[0],eye[3])

    # EAR 알고리즘을 활용한 졸음 인식
    # EAR = |p2 - p6| + |p3 - p5| / 2 * |p1 - p4|
    ear = (A + B) / (2.0 * C)

    return ear

# construct the argument parse and parse the arguments
# 파이썬 호출 당시 인자값을 줘서 동작을 다르게 하고 싶을 떄 사용 - argparse

# 인자값 받을 수 있는 인스턴스 생성
ap = argparse.ArgumentParser()

# add_argument : 입력받을 인자값을 등록하는 함수
ap.add_argument("-p", "--shape-predictor", required=True,help="path to facial landmark predictor")
ap.add_argument("-a", "--alarm",type=str,default="",help="path alarm .WAV file")
ap.add_argument("-w", "--webcam",type=int,default=0,help="index of webcam on system")

# 입력받은 인자값을 args에 저장
# vars : 인스턴스의 속성을 dictionary 형태로 보여준다
args = vars(ap.parse_args())

EYE_AR_THRESH = 0.3 # 사용자의 눈 측정 임계값, 이보다 작으면 졸린 것으로 판단
EYE_AR_CONSEC_FRAMES = 48 # 사용자가 임계값보다 작은 수치로 있는 프레임 수

# 알람이 울리고 있는지, 얼마나 울렸는지 판별하는 변수
COUNTER = 0
ALARM_ON = False 

# dlib의 face detector, facial landmark predictor 인스턴스 생성
print("[INFO] loading facial landmark predictor...")
detector = dlib.get_frontal_face_detector() 
# 여기서 처음에 argparse로 받은 학습된 dat 파일이 들어간다
predictor = dlib.shape_predictor(args["shape_predictor"])

# grab the indexes of the facial landmarks for the left and
# right eye, respectively
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

# Video stream thread 시작
print("[INFO] starting video stream thread...")
# Pi camera 사용하려면 webcam arg에 0보다 큰 정수 입력
vs = VideoStream(src=args["webcam"]).start()
time.sleep(2.0)

# loop 함수 내에서 video streaming 관련 처리
while True:
    # grab the frame from the threaded video stream
    # resize - max : 400 pixel
    # convert it to grayscale
    # grayscale로 바꾸는 이유 - 노이즈 제거 및 연산 속도 증가, 정확도 향상
    frame = vs.read()
    frame = imutils.resize(frame,width = 400)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # detect faces in the grayscale frame
    rects = detector(gray, 0)

    # face detection 후 해당 face에 대한 처리
    for rect in rects:
        # determine the facial landmarks for the face region, then
		# convert the facial landmark (x, y)-coordinates to a NumPy
		# array
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)

        # 왼쪽 눈과 오른쪽 눈의 좌표계를 추출해 낸다
        # EAR 알고리즘에 적용시킨다
        leftEye = shape[lStart:lEnd]
        rightEye = shape[rStart:rEnd]
        leftEAR = eye_aspect_ratio(leftEye)
        rightEAR = eye_aspect_ratio(rigthEye)

        # 양쪽 눈의 EAR 값의 평균값을 구한다
        ear = (leftEAR + rightEAR) / 2.0

        # cv2.drawContours : 윤곽선을 그리는 opencv 함수
        # compute the convex hull for the left and right eye, then
		# visualize each of the eyes
        # cv2.convexHull : 윤곽선의 경계면을 둘러싸는 다각형을 구하는 알고리즘
        leftEyeHull = cv2.convexHull(leftEye)
        rightEyeHull = cv2.convexHull(rightEye)
        cv2.drawContours(frame,[leftEyeHull],-1,(0,255,0),1)
        cv2.drawContours(frame,[rightEyeHull],-1,(0,255,0),1)

