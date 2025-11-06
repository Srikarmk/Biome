import cv2
import mediapipe as mp
from utils.angle import calculate_angle
from utils.logger import log_result
from utils.sound import speak
mp_pose = mp.solutions.pose
mp_draw = mp.solutions.drawing_utils

def run_squat():
    cap = cv2.VideoCapture(0)
    counter = 0
    state = "up"   
    feedback = ""

    SQUAT_DOWN_ANGLE = 90       
    SQUAT_UP_ANGLE = 160      
    BACK_STRAIGHT_ANGLE = 150 

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

                hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                       landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                        landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                         landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
                shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                            landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]

                knee_angle = calculate_angle(hip, knee, ankle)
                back_angle = calculate_angle(shoulder, hip, ankle)

                last_feedback = ""
                if back_angle < BACK_STRAIGHT_ANGLE:
                    feedback = "KEEP BACK STRAIGHT"
                else:
                    feedback = "GOOD FORM"

                if knee_angle < SQUAT_DOWN_ANGLE and state == "up":
                    state = "down"
                    feedback = "LOW ENOUGH - NOW STAND UP"

                if knee_angle > SQUAT_UP_ANGLE and state == "down":
                    state = "up"
                    counter += 1
                    feedback = "REP COUNTED!"
                if feedback != last_feedback:
                    speak(feedback)
                    last_feedback = feedback
            except:
                feedback = "NO BODY DETECTED"
                
            if feedback != last_feedback:
                speak(feedback)
                last_feedback = feedback

            cv2.putText(image, f"REPS: {counter}", (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255,255,255), 3)

            cv2.putText(image, f"FORM: {feedback}", (10, 110),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

            cv2.putText(image, f"KNEE ANGLE: {int(knee_angle)}", (10, 150),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)

            if results.pose_landmarks:
                mp_draw.draw_landmarks(image, results.pose_landmarks,
                                       mp_pose.POSE_CONNECTIONS)

            cv2.imshow('Squat Trainer', image)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()

    log_result("squat", counter)

    print(f"Total Squats: {counter}")
    return counter
