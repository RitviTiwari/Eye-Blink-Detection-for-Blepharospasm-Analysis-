# Eye-Blink-Detection-for-Blepharospasm-Analysis-

# Overview:
This project focuses on detecting abnormal blinking patterns to identify potential cases of blepharospasm, a condition characterized by involuntary eye blinking. Using real-time eye aspect ratio (EAR) calculations, the system accurately counts blinks and provides insights for medical applications.

# Features:

- **Real-Time Blink Detection:** Leverages webcam input to process and analyze eye blinks in real-time. 

- **EAR Calculation:** Uses Eye Aspect Ratio (EAR) to determine blinking events and detect abnormal blinking rates.
  
- **Blepharospasm Analysis:** Classifies blinking rates to detect potential signs of blepharospasm.

# Technologies Used

. **Programming Language: Python**

# Libraries:

- **OpenCV:** For image and video processing.

- **Dlib:** For facial landmark detection.

- **NumPy:** For mathematical computations.

# How It Works:

1.The system uses dlib to detect facial landmarks, including the eyes.

2.The Eye Aspect Ratio (EAR) is computed using the distances between specific eye landmarks.

3.A blink is detected when the EAR falls below a predefined threshold.

4.Blinking rates are monitored over a fixed time period to determine if they exceed normal levels.

5.If blinking exceeds a defined threshold (e.g., 20 blinks per minute), the system flags a potential case of blepharospasm.

