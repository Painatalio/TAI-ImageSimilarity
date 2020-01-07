# Code developed by Pedro Ferreira, Rafael Direito e Rafael Teixeira

import os
import sys
import cv2
sys.path.append('../classifier')
import ncdC
import time
from PIL import Image


"""
Class responsible for the facial recognition using the computer camera.
"""
class CameraRecog:
    """
    Function to detect and recognize someone using the laptop camera.
    deviceID, is the ID of the camera plugged to the computer, usually is 0 (the first camera).
    apiID, is the API backend to be used, the default is CV_CAP_ANY = 0, which autodetects default API.
    """
    def live_face_recognition(self, images_path, algorithm, threshold, deviceID=0, apiID=0):
        if not os.path.exists(images_path):
            print("ERROR: The provided folder doesn't exist!")
            return

        images = []

        for image in os.listdir(images_path):
            if not ".png" in image:
                print("ERROR: Found a non png file.")
                return

            # Read each image which contains the subject that will be compared to.
            images.append((image, Image.open(images_path + image)))

        # Store the name of the images which the ncd result was lower than the threshold.
        recognized_images = []

        ncd = ncdC.Ncd(algorithm)

        # Initialize the video capture.
        cap = cv2.VideoCapture()

        # Open the selected camera, using the selected API.
        cap.open(deviceID, apiID)

        # Initialize the face recognizer (default face haar cascade).
        face_cascade = cv2.CascadeClassifier("cascades/haarcascade_frontalface_default.xml")

        print("Press the key 'q' to exit the live preview!")

        start_passed = time.time()

        recognize = False

        taken_pictures = 0

        while True:
            # Read the next frame of the camera.
            _, frame = cap.read()

            # Convert the frame to grayscale.
            image_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Detect all the faces on the frame.
            faces = face_cascade.detectMultiScale(image_gray, 1.3, 5)

            face_id = 0

            # Recognize every two seconds.
            if time.time() - start_passed >= 2:
                recognize = True
                recognized_images = []
                start_passed = time.time()

            for x, y, width, height in faces:
                if recognize:
                    # Retrieve only the face from the frame with gray tones.
                    face = image_gray[y:y+height, x:x+width]
                    face_resized = cv2.resize(face, (150, 150), interpolation=cv2.INTER_AREA)
                    ncd_results = []

                    for image in images:
                        image_resized = image[1].resize((150, 150))
                        ncd_results.append(ncd.classify([image_resized], Image.fromarray(face_resized)))

                    if min(ncd_results) < threshold:
                        recognized_images.append(images[ncd_results.index(min(ncd_results))][0])

                # Draws a red rectangle on every face present in the frame, which was not recognized.
                if not recognized_images:
                    cv2.rectangle(frame, (x, y), (x + width, y + height), color=(0, 0, 255), thickness=2)
                # Draws a blue rectangle on every face present in the frame, which was recognized.
                else:
                    if face_id < len(recognized_images):
                        rect = cv2.rectangle(frame, (x, y), (x + width, y + height), color=(255, 0, 0), thickness=2)
                        cv2.putText(rect, recognized_images[face_id], (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color=(255, 0, 0), thickness=2)
                face_id += 1

            if recognize:
                cv2.imwrite(images_path + "Img" + str(taken_pictures) + ".png", frame)
                taken_pictures += 1

            recognize = False

            # Create a window with the title 'live-preview' and displays the frame.
            cv2.imshow("live-preview", frame)

            # If the key 'q' is pressed, the live preview stops and the window is closed.
            if cv2.waitKey(1) == ord("q"):
                break

        # Release the camera.
        cap.release()

        # Close any remaining windows that could be open.
        cv2.destroyAllWindows()

    """
    Function to take pictures with the laptop camera.
    """
    def take_pictures(self, deviceID=0, apiID=0, name_prefix="Image", save_path="../../images/webcam_images/"):
        # If the folder doesn't exist, create it.
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        # Initialize the video capture.
        cap = cv2.VideoCapture()

        # Open the selected camera, using the selected API.
        cap.open(deviceID, apiID)

        # Initialize the face recognizer (default face haar cascade).
        face_cascade = cv2.CascadeClassifier("cascades/haarcascade_frontalface_default.xml")

        taken_pictures = 0

        print("Press 'q' to exit the program, or any other key to take a picture!")
        
        while True:
            # Read the next frame of the camera.
            _, frame = cap.read()

            # Convert the frame to grayscale.
            image_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Detect all the faces on the frame.
            faces = face_cascade.detectMultiScale(image_gray, 1.3, 5)

            # Create a window with the title 'live-preview' and displays the frame.
            cv2.imshow("live-preview", frame)

            pressed_key = cv2.waitKey(1)

            # If the key 'q' is pressed, live preview stops and the window is closed.
            if pressed_key == ord("q"):
                break
            # If any other key is pressed, take a picture and save it.
            elif pressed_key != -1:
                for x, y, width, height in faces:
                    # Retrieve only the face from the frame with gray tones.
                    face = image_gray[y:y+height, x:x+width]

                    # Saves the image on disk.
                    cv2.imwrite(save_path + name_prefix + str(taken_pictures) + ".png", face)
                    print("Picture " + str(taken_pictures) + " taken and saved!")
                    taken_pictures += 1

        # Release the camera.
        cap.release()

        # Close any remaining windows that could be open.
        cv2.destroyAllWindows()


if __name__ == '__main__':
    camera = CameraRecog()

    if len(sys.argv) > 1 and int(sys.argv[1]) == 0:
        if len(sys.argv) == 2:
            camera.take_pictures()
        elif len(sys.argv) == 3:
            camera.take_pictures(int(sys.argv[2]))
        elif len(sys.argv) == 4:
            camera.take_pictures(int(sys.argv[2]), int(sys.argv[3]))
        elif len(sys.argv) == 5:
            camera.take_pictures(int(sys.argv[2]), int(sys.argv[3]), sys.argv[4])
        elif len(sys.argv) == 6:
            camera.take_pictures(int(sys.argv[2]), int(sys.argv[3]), sys.argv[4], sys.argv[5])

        sys.exit(0)
    elif len(sys.argv) > 4 and int(sys.argv[1]) == 1:
        if len(sys.argv) == 5:
            camera.live_face_recognition(sys.argv[2], sys.argv[3], float(sys.argv[4]))
        elif len(sys.argv) == 6:
            camera.live_face_recognition(sys.argv[2], sys.argv[3], float(sys.argv[4]), int(sys.argv[5]))
        elif len(sys.argv) == 7:
            camera.live_face_recognition(sys.argv[2], sys.argv[3], float(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6]))
        sys.exit(0)
    else:
        print("Program usage to take pictures: python3 main.py 0 optional: <deviceID> <apiID> <prefix name of the image> <path to save the images>\n")
        print("Program usage for the face recognition: python3 main.py 1 <path to extract the images from> <algorithm> <threshold> optional: <deviceID> <apiID>")
        sys.exit(1)
