import cv2
import dlib
import numpy as np
import time

# Load the pre-trained facial landmark detector
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# Initialize the camera
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Camera not opening!")
    exit()

# Function to calculate Eye Aspect Ratio (EAR)
def get_eye_aspect_ratio(eye):
    A = np.linalg.norm(eye[1] - eye[5])  # Vertical distance
    B = np.linalg.norm(eye[2] - eye[4])  # Vertical distance
    C = np.linalg.norm(eye[0] - eye[3])  # Horizontal distance
    return (A + B) / (2.0 * C)

# Initialize variables
blink_counter = 0
start_time = time.time()
blink_threshold = 0.22  # Adjusted for accuracy
blink_detected = False

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)

    for face in faces:
        landmarks = predictor(gray, face)

        # Get coordinates for eyes
        left_eye = np.array([(landmarks.part(i).x, landmarks.part(i).y) for i in range(36, 42)])
        right_eye = np.array([(landmarks.part(i).x, landmarks.part(i).y) for i in range(42, 48)])

        # Calculate EAR for both eyes
        left_ear = get_eye_aspect_ratio(left_eye)
        right_ear = get_eye_aspect_ratio(right_eye)
        ear = (left_ear + right_ear) / 2.0

        # Blink detection
        if ear < blink_threshold:
            blink_detected = True
        else:
            if blink_detected:
                blink_counter += 1
                blink_detected = False

    # Display "Blink Detected" in real time
    if blink_detected:
        cv2.putText(frame, "Blink Detected!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

    # Calculate elapsed time
    elapsed_time = time.time() - start_time

    # If 1 minute has passed, display results
    if elapsed_time >= 60:
        result_text = f"Total Blinks in 1 Minute: {blink_counter}"
        if blink_counter > 15:
            detection_text = "Blepharospasm Detected!"
            result_color = (0, 0, 255)  # Red
        else:
            detection_text = "No Blepharospasm Detected!"
            result_color = (0, 255, 0)  # Green

        # Display results at the top center
        frame_height, frame_width = frame.shape[:2]
        center_x = frame_width // 2

        end_time = time.time()
        while time.time() - end_time < 10:
            frame_with_result = frame.copy()
            # Display total blinks
            cv2.putText(frame_with_result, result_text, (center_x - 300, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            # Display detection result
            cv2.putText(frame_with_result, detection_text, (center_x - 300, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, result_color, 2)
            cv2.imshow("Live Video", frame_with_result)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cap.release()
                cv2.destroyAllWindows()
                exit()

        # Reset counters for the next minute
        blink_counter = 0
        start_time = time.time()

    # Resize the window to square dimensions
    square_size = 500  # Set both width and height to 500 for square dimensions
    frame_resized = cv2.resize(frame, (square_size, square_size))
    cv2.imshow("Live Video", frame_resized)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
