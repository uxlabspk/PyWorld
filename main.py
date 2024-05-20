import cv2 
import mediapipe as mp
import pyautogui

def main():
    # Initialize the webcam (cv2.VideoCapture) and check if it's opened successfully.
    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        print("Error: Unable to open camera.")
        return

    # Initialize MediaPipe's FaceMesh solution with refined landmarks.
    face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
    # Get the screen size using PyAutoGUI.
    screen_w, screen_h = pyautogui.size()

    # Enter a while loop to continuously read frames from the webcam.
    while True:
        # Read a frame from the webcam.
        _, frame = cam.read()
        if frame is None:
            break

        #  flip the frames horizontally.
        frame = cv2.flip(frame, 1)
        # Convert the frame from BGR to RGB colors.
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Process the RGB frame using MediaPipe's FaceMesh and get the landmark points.
        output = face_mesh.process(rgb_frame)
        landmark_points = output.multi_face_landmarks
        frame_h, frame_w, _ = frame.shape

        # Extract the coordinates of specific landmarks (left eye) and draw circles around them.
        if landmark_points:
            landmarks = landmark_points[0].landmark
            for id, landmark in enumerate(landmarks[474:478]):
                x = int(landmark.x * frame_w)
                y = int(landmark.y * frame_h)
                cv2.circle(frame, (x, y), 3, (0, 255, 0))
                if id == 1:
                    screen_x = screen_w * landmark.x
                    screen_y = screen_h * landmark.y
                    # moving the cursor to screen.
                    pyautogui.moveTo(screen_x, screen_y)

            # Left eye landmarks.
            left = [landmarks[145], landmarks[159]]
            for landmark in left:
                x = int(landmark.x * frame_w)
                y = int(landmark.y * frame_h)
                # draw circles on left eye.
                cv2.circle(frame, (x, y), 3, (0, 255, 255))
                
            # Here, error comes.    
            # right = [landmarks[164], landmarks[264]]   # 33 -> 263
            # for landmark in right:
            #    x = int(landmark.x * frame_w)
            #    y = int(landmark.y * frame_h)
            #    cv2.circle(frame, (x, y), 3, (255, 0, 255))

            # Calculate the vertical distance between two landmarks 
            # in the left eye to determine if the user wants to click.
            if (left[0].y - left[1].y) < 0.008: #0.004:
                # click on screen when left eye is closed.
                pyautogui.click()

            # elif (right[0].y - right[1].y) < 0.006:
            #    pyautogui.click(button='right')

        # Showing the screen and frames.
        # when we press the 'q' the program exit.
        cv2.imshow('Eye Controlled Mouse', frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):  # Press 'q' to quit
            break

    # release the camera resource and destroy the screen.
    cam.release()
    cv2.destroyAllWindows()

# Call the main() function if the script is run as the main program.
if __name__ == "__main__":
    main()

