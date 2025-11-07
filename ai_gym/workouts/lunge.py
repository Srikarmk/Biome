import cv2
import mediapipe as mp
from utils.angle import calculate_angle
from utils.logger import log_result
from utils.sound import speak 

mp_pose = mp.solutions.pose
mp_draw = mp.solutions.drawing_utils

def run_lunge():
    cap = cv2.VideoCapture(0)

    counter = 0
    state = "up" 
    feedback = "GET INTO START POSITION"
    

    DOWN_ANGLE = 95       
    UP_ANGLE = 150        
    KNEE_ALIGNMENT_LIMIT = 0.04  

    with mp_pose.Pose(min_detection_confidence=0.6,
                      min_tracking_confidence=0.6) as pose:

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            h, w, _ = frame.shape
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(image)
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            active_leg_angle = None
            angle_text = "--"
            last_feedback = ""

            if results.pose_landmarks is None:
                feedback = "NO BODY DETECTED"
            else:
                try:
                    landmarks = results.pose_landmarks.landmark

                   
                    l_hip = (landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                             landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y)
                    l_knee = (landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                              landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y)
                    l_ankle = (landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                               landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y)

                    
                    r_hip = (landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                             landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y)
                    r_knee = (landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                              landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y)
                    r_ankle = (landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
                               landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y)

                   
                    left_knee_angle = calculate_angle(l_hip, l_knee, l_ankle)
                    right_knee_angle = calculate_angle(r_hip, r_knee, r_ankle)

                    if left_knee_angle <= right_knee_angle:
                        active_leg = "left"
                        active_leg_angle = left_knee_angle
                        knee_x_shift = abs(l_knee[0] - l_ankle[0])
                    else:
                        active_leg = "right"
                        active_leg_angle = right_knee_angle
                        knee_x_shift = abs(r_knee[0] - r_ankle[0])

                    angle_text = str(int(active_leg_angle))

                    if knee_x_shift > KNEE_ALIGNMENT_LIMIT:
                        feedback = "KNEE IN LINE WITH ANKLE"
                    else:
                        feedback = "GOOD FORM"

                    if active_leg_angle < DOWN_ANGLE and state == "up":
                        state = "down"
                        feedback = "GOING DOWN"

                    if active_leg_angle > UP_ANGLE and state == "down":
                        state = "up"
                        counter += 1
                        feedback = "REP COUNTED!"

                except Exception:
                    feedback = "POSE READ ERROR"

            if feedback != last_feedback:
                speak(feedback)
                last_feedback = feedback

            cv2.putText(image, f"REPS: {counter}", (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255,255,255), 3)

            cv2.putText(image, feedback, (10, 110),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

            cv2.putText(image, f"ANGLE: {angle_text}", (10, 150),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)

            if results.pose_landmarks:
                mp_draw.draw_landmarks(image, results.pose_landmarks,
                                       mp_pose.POSE_CONNECTIONS)

            cv2.imshow("Lunge Trainer", image)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()

    log_result("lunge", counter)
    print(f"Total Lunges: {counter}")

    return counter
