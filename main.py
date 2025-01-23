import cv2
import mediapipe as mp
import random
import time

# Initialize Mediapipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Define questions and answers
questions = [
    {"question": "Python is a programming language?", "answer": "True"},
    {"question": "The capital of France is Berlin?", "answer": "False"},
    {"question": "The Sun rises in the west?", "answer": "False"},
    {"question": "OpenCV is used for computer vision?", "answer": "True"},
    {"question": "2 + 2 = 5?", "answer": "False"}
]

# Function to detect gestures (Thumbs-Up or Thumbs-Down)
def detect_gesture(hand_landmarks):
    # Landmark indexes for thumb tip and index finger tip
    THUMB_TIP = 4
    INDEX_TIP = 8

    # Thumb tip coordinates
    thumb_tip = hand_landmarks.landmark[THUMB_TIP]
    index_tip = hand_landmarks.landmark[INDEX_TIP]

    # Compare y-coordinates of thumb tip and index tip
    if thumb_tip.y < index_tip.y:  # Thumb up
        return "True"
    else:  # Thumb down
        return "False"

# Main game logic
def quiz_game():
    cap = cv2.VideoCapture(0)  # Open webcam
    score = 0  # Initialize score
    question_index = 0  # Current question index

    # Display each question for 10 seconds
    time_limit = 10

    while question_index < len(questions):
        question = questions[question_index]
        start_time = time.time()

        while time.time() - start_time < time_limit:
            ret, frame = cap.read()  # Read frame from webcam
            if not ret:
                print("Failed to capture video")
                break

            frame = cv2.flip(frame, 1)  # Flip the frame for a mirrored view
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert to RGB for Mediapipe
            results = hands.process(rgb_frame)  # Process the frame with Mediapipe

            # Display the question
            cv2.putText(frame, f"Question: {question['question']}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(frame, "Show Thumbs-Up for True, Thumbs-Down for False", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)

            # If hands are detected
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Draw hand landmarks
                    mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                    # Detect gesture
                    gesture = detect_gesture(hand_landmarks)

                    # Display detected gesture
                    cv2.putText(frame, f"Detected Gesture: {gesture}", (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

                    # Check if gesture matches the answer
                    if gesture == question["answer"]:
                        score += 1
                        question_index += 1
                        cv2.putText(frame, "Correct!", (10, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
                        time.sleep(1)  # Pause to show feedback
                        break
                    elif gesture != question["answer"]:
                        question_index += 1
                        cv2.putText(frame, "Incorrect!", (10, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                        time.sleep(1)  # Pause to show feedback
                        break

            # Show the frame
            cv2.imshow("Quiz Game", frame)

            # Exit the game on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        question_index += 1  # Move to the next question

    cap.release()
    cv2.destroyAllWindows()

    # Display the final score
    print(f"Game Over! Your final score is {score}/{len(questions)}")

# Run the game
if __name__ == "__main__":
    quiz_game()
