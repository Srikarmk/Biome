"""
Real-time Push-up Counter and Form Analyzer
Uses MediaPipe Pose for pose estimation and form feedback
"""

import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

# Configuration constants
ELBOW_EXTENDED_ANGLE = 155
ELBOW_BENT_ANGLE = 90
BACK_STRAIGHT_ANGLE = 145
ELBOW_TUCK_THRESHOLD = 65
VISIBILITY_THRESHOLD = 0.8


def calculate_angle(a, b, c):
    """
    Calculate angle at point b formed by points a-b-c
    
    Args:
        a, b, c: Lists/arrays with [x, y] coordinates
    
    Returns:
        float: Angle in degrees (0-180)
    """
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    
    if angle > 180.0:
        angle = 360 - angle
    
    return angle


def main():
    """Main function to run the push-up tracking system"""
    
    # Initialize video capture
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open camera")
        print("Make sure your webcam is connected and not being used by another application")
        return
    
    # Get frame dimensions
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    
    print(f"Camera initialized: {frame_width}x{frame_height}")
    print("Press 'q' to quit, 'r' to reset counter")
    
    # Video writer setup
    output_path = 'Recap.mp4'
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, 20.0, (frame_width, frame_height))
    
    if not out.isOpened():
        print("Warning: Could not initialize video writer. Recording disabled.")
    
    # State variables
    counter = 0
    state = 'get_ready'
    feedback = ''
    
    with mp_pose.Pose(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    ) as pose:
        
        while cap.isOpened():
            ret, frame = cap.read()
            
            if not ret:
                print("Failed to grab frame")
                break
            
            # Prepare image for processing
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = pose.process(image)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            # Initialize angles
            avg_back_angle = 0
            avg_elbow_angle = 0
            
            try:
                landmarks = results.pose_landmarks.landmark
                
                # Get landmark values
                l_shoulder_val = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
                l_elbow_val = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value]
                l_wrist_val = landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value]
                l_hip_val = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
                l_ankle_val = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value]
                
                r_shoulder_val = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
                r_elbow_val = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value]
                r_wrist_val = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value]
                r_hip_val = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]
                r_ankle_val = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value]
                
                # Check body visibility
                is_body_visible = all(
                    lm.visibility > VISIBILITY_THRESHOLD 
                    for lm in [l_shoulder_val, l_elbow_val, l_hip_val, 
                              r_shoulder_val, r_elbow_val, r_hip_val]
                )
                
                # Extract coordinates
                l_shoulder = [l_shoulder_val.x, l_shoulder_val.y]
                l_elbow = [l_elbow_val.x, l_elbow_val.y]
                l_wrist = [l_wrist_val.x, l_wrist_val.y]
                l_hip = [l_hip_val.x, l_hip_val.y]
                l_ankle = [l_ankle_val.x, l_ankle_val.y]
                
                r_shoulder = [r_shoulder_val.x, r_shoulder_val.y]
                r_elbow = [r_elbow_val.x, r_elbow_val.y]
                r_wrist = [r_wrist_val.x, r_wrist_val.y]
                r_hip = [r_hip_val.x, r_hip_val.y]
                r_ankle = [r_ankle_val.x, r_ankle_val.y]
                
                # Calculate angles
                avg_elbow_angle = (
                    calculate_angle(l_shoulder, l_elbow, l_wrist) + 
                    calculate_angle(r_shoulder, r_elbow, r_wrist)
                ) / 2
                
                avg_back_angle = (
                    calculate_angle(l_shoulder, l_hip, l_ankle) + 
                    calculate_angle(r_shoulder, r_hip, r_ankle)
                ) / 2
                
                # Check form
                form_feedback = "GOOD FORM"
                if (calculate_angle(l_hip, l_shoulder, l_elbow) > ELBOW_TUCK_THRESHOLD or 
                    calculate_angle(r_hip, r_shoulder, r_elbow) > ELBOW_TUCK_THRESHOLD):
                    form_feedback = "TUCK ELBOWS"
                
                # State machine logic (FIXED VERSION)
                if state == 'get_ready':
                    if is_body_visible and avg_back_angle > BACK_STRAIGHT_ANGLE and avg_elbow_angle > ELBOW_EXTENDED_ANGLE:
                        state = 'ready'
                        feedback = form_feedback
                    else:
                        feedback = "GET INTO PLANK POSITION"
                
                elif state == 'ready':
                    # FIX: Added this state transition that was missing!
                    feedback = form_feedback
                    if avg_elbow_angle < ELBOW_EXTENDED_ANGLE:
                        state = 'down'
                
                elif state == 'down':
                    feedback = form_feedback
                    if avg_elbow_angle > ELBOW_EXTENDED_ANGLE:
                        counter += 1
                        state = 'ready'
                        feedback = "REP COUNTED!"
            
            except Exception as e:
                state = 'get_ready'
                feedback = "NO BODY DETECTED"
            
            # Determine feedback box color
            if "TUCK ELBOWS" in feedback:
                feedback_box_color = (0, 0, 255)  # Red
            elif "GOOD" in feedback:
                feedback_box_color = (0, 150, 0)  # Green
            elif "COUNTED" in feedback:
                feedback_box_color = (200, 100, 0)  # Blue-ish
            elif "DETECTED" in feedback:
                feedback_box_color = (0, 165, 255)  # Orange
            else:
                feedback_box_color = (128, 0, 0)  # Dark blue
            
            # Draw UI elements
            # Counter box
            cv2.rectangle(image, (0, 0), (250, 73), (50, 50, 50), -1)
            cv2.putText(image, 'REPS', (15, 20), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
            cv2.putText(image, str(counter), (10, 60), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2, cv2.LINE_AA)
            
            # Status box
            cv2.putText(image, 'STATUS', (130, 20), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
            cv2.putText(image, state.upper(), (120, 60), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
            
            # Feedback box (dynamic width based on frame)
            feedback_box_width = frame_width - 250
            cv2.rectangle(image, (250, 0), (frame_width, 73), feedback_box_color, -1)
            
            (text_width, _), _ = cv2.getTextSize(feedback, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
            text_x = 250 + (feedback_box_width - text_width) // 2
            cv2.putText(image, feedback, (text_x, 45), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
            
            # Angle displays
            cv2.putText(image, f"BACK: {int(avg_back_angle)}", 
                       (15, frame_height - 50), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(image, f"ELBOW: {int(avg_elbow_angle)}", 
                       (15, frame_height - 20), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv2.LINE_AA)
            
            # Draw pose landmarks
            if results.pose_landmarks:
                mp_drawing.draw_landmarks(
                    image, 
                    results.pose_landmarks, 
                    mp_pose.POSE_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                    mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
                )
            
            # Write frame to output video
            if out.isOpened():
                out.write(image)
            
            # Display the frame
            cv2.imshow('Push-Up Trainer', image)
            
            # Handle keyboard input
            key = cv2.waitKey(10) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('r'):
                counter = 0
                state = 'get_ready'
                print("Counter reset")
    
    # Cleanup
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    
    print(f"\nSession complete!")
    print(f"Total reps: {counter}")
    print(f"Video saved to: {output_path}")


if __name__ == "__main__":
    main()




