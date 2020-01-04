# Code developed by Pedro Ferreira, Rafael Direito e Rafael Teixeira

import os
import cv2


"""
Function to detect and recognize someone using the laptop camera.
deviceID, is the ID of the camera plugged to the computer, usually is 0 (the first camera).
apiID, is the API backend to be used, the default is CV_CAP_ANY = 0, which autodetects default API.
"""
def live_face_recognition(deviceID=0, apiID=0):
    # Initialize the video capture.
    cap = cv2.VideoCapture()

    # Open the selected camera, using the selected API.
    cap.open(deviceID, apiID)

    # Initialize the face recognizer (default face haar cascade).
    face_cascade = cv2.CascadeClassifier("cascades/haarcascade_frontalface_default.xml")

    print("Press any key to exit the live preview!")

    while True:
        # Read the next frame of the camera.
        _, frame = cap.read()

        # Convert the frame to grayscale.
        image_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect all the faces on the frame.
        faces = face_cascade.detectMultiScale(image_gray, 1.3, 5)

        # Draws a blue rectangle on every face present in the frame.
        for x, y, width, height in faces:
            cv2.rectangle(frame, (x, y), (x + width, y + height), color=(255, 0, 0), thickness=2)

        # Create a window with the title 'live-preview' and displays the frame.
        cv2.imshow("live-preview", frame)

        # If any key is pressed, the live preview stops and the window is closed.
        if cv2.waitKey(1) != -1:
            break

    # Release the camera.
    cap.release()

    # Close any remaining windows that could be open.
    cv2.destroyAllWindows()


"""
Function to take pictures with the laptop camera.
"""
def take_pictures(deviceID=0, apiID=0, name_prefix="Test", save_path="../webcam_images/"):
    # If the folder doesn't exist, create it.
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    # Initialize the video capture.
    cap = cv2.VideoCapture()

    # Open the selected camera, using the selected API.
    cap.open(deviceID, apiID)

    taken_pictures = 0

    print("Press 'q' to exit the program, or any other key to take a picture!")
    
    while True:
        # Read the next frame of the camera.
        _, frame = cap.read()

        # Create a window with the title 'live-preview' and displays the frame.
        cv2.imshow("live-preview", frame)

        pressed_key = cv2.waitKey(1)

        # If the key 'q' is pressed, live preview stops and the window is closed.
        if pressed_key == ord("q"):
            break
        # If any other key is pressed, take a picture and save it.
        elif pressed_key != -1:
            cv2.imwrite(save_path + name_prefix + str(taken_pictures) + ".jpg", frame)
            print("Picture " + str(taken_pictures) + " taken and saved!")
            taken_pictures += 1

    # Release the camera.
    cap.release()

    # Close any remaining windows that could be open.
    cv2.destroyAllWindows()        

