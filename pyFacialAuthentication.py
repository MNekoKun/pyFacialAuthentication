from colors import colors
import sys
import cv2
import face_recognition

def check_face():
    print("Getting password image... ", end="")
    try:
        image = face_recognition.load_image_file("img/password.jpg")
        print(colors.OK + colors.BOLD + "OK" + colors.DEFAULT)
    except FileNotFoundError:
        print(colors.FAIL + colors.BOLD + "\nNo image found" + colors.DEFAULT)
        sys.exit(1)
    #get the face encoding
    face_encoding = face_recognition.face_encodings(image)[0]
    #take a photo from the webcam and save it as img/webcam.jpg
    webcam = cv2.VideoCapture(0)
    return_value, image = webcam.read()
    cv2.imwrite("img/webcam.jpg", image)
    del(webcam)
    #load the webcam image
    webcam_image = face_recognition.load_image_file("img/webcam.jpg")
    #get the webcam face encoding
    try:
        webcam_face_encoding = face_recognition.face_encodings(webcam_image)[0]
    except IndexError:
        print("No face found")
        return
    #compare the two faces
    results = face_recognition.compare_faces([face_encoding], webcam_face_encoding)
    #print the results
    print(results)

def main():
    print(colors.DONE + colors.BOLD + colors.UNDERLINE + "pyFacialAuthentication\n" + colors.DEFAULT)
    authorized = check_face()

if __name__ == "__main__":
    main()