import cv2
import time
import mediapipe as mp
from utils.angle import calculate_angle
from utils.logger import log_result
from utils.sound import speak
mp_pose = mp.solutions.pose
mp_draw = mp.solutions.drawing_utils

def run_plank():
    cap = cv2.VideoCapture(0)

    feedback = "GET INTO PLANK POSITION"
    holding = False
    start_time = 0
    hold_duration = 0

    BACK_STRAIGHT_MIN_ANGLE = 145  

    with mp_pose.Pose(min_detection_confidence=0.5,
                      min_tracking_confidence=0.5) as pose:

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(image)
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            last_feedback = ""

            try:
                landmarks = results.pose_landmarks.landmark

                shoulder = [
                    landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                    landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y
                ]
                hip = [
                    landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                    landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y
                ]
                ankle = [
                    landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                    landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y
                ]

                back_angle = calculate_angle(shoulder, hip, ankle)

                if back_angle > BACK_STRAIGHT_MIN_ANGLE:
                    feedback = "HOLD - GOOD FORM"
                    if not holding:
                        holding = True
                        start_time = time.time()
                else:
                    feedback = "CORRECT YOUR FORM"
                    if holding:
                        holding = False
                        hold_duration += time.time() - start_time

            except:
                feedback = "NO BODY DETECTED"
                if holding:
                    holding = False
                    hold_duration += time.time() - start_time
                    
            if feedback != last_feedback:
                speak(feedback)
                last_feedback = feedback
            total_time = hold_duration
            if holding:
                total_time += time.time() - start_time

            time_display = time.strftime("%M:%S", time.gmtime(total_time))

            cv2.putText(image, f"TIME: {time_display}", (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255,255,255), 3)

            cv2.putText(image, feedback, (10, 110),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

            if results.pose_landmarks:
                mp_draw.draw_landmarks(image, results.pose_landmarks,
                                       mp_pose.POSE_CONNECTIONS)

            cv2.imshow('Plank Trainer', image)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()

    if holding:
        hold_duration += time.time() - start_time

    total_time = time.strftime("%M:%S", time.gmtime(hold_duration))

    log_result("plank", total_time)
    print(f"Total Plank Hold Time: {total_time}")

    return total_time
