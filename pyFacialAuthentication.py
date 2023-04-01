from colors import colors
import sys
import os
import cv2
import face_recognition

def check_face():
    print("Getting password image... ", end="")
    try:
        image = face_recognition.load_image_file("password.jpg")
        print(colors.OK + colors.BOLD + "OK" + colors.DEFAULT)
    except FileNotFoundError:
        print(colors.FAIL + colors.BOLD + "\nNo image found" + colors.DEFAULT)
        sys.exit(1)
    
    password_faces = face_recognition.face_encodings(image)
    if len(password_faces) == 0:
        print(colors.FAIL + colors.BOLD + "No faces found" + colors.DEFAULT)
        sys.exit(1)
    elif len(password_faces) > 1:
        print(colors.WARNING + colors.BOLD + "WARNING: " + colors.DEFAULT + colors.WARNING + "More than one face found" + colors.DEFAULT)
        password_face_index = int(input("Which face do you want to use? >"))
        password_face_index -= 1
        if 0>password_face_index or password_face_index>=len(password_faces):
            print(colors.FAIL + colors.BOLD + "Invalid index" + colors.DEFAULT)
            sys.exit(1)
    else:
        password_face_index = 0
    
    print("Getting webcam image... ", end="")
    try:
        webcam = cv2.VideoCapture(0)
        return_value, image = webcam.read()
    except:
        print(colors.FAIL + colors.BOLD + "Something went wrong during webcam capture" + colors.DEFAULT)
        sys.exit(1)
    cv2.imwrite("webcam.jpg", image)
    del(webcam)
    webcam_image = face_recognition.load_image_file("webcam.jpg")
    print(colors.OK + colors.BOLD + "OK" + colors.DEFAULT)

    webcam_faces = face_recognition.face_encodings(webcam_image)
    if len(webcam_faces) == 0:
        print(colors.FAIL + colors.BOLD + "No faces found" + colors.DEFAULT)
        sys.exit(1)
    elif len(webcam_faces) > 1:
        print(colors.WARNING + colors.BOLD + "WARNING: " + colors.DEFAULT + colors.WARNING + "More than one face found" + colors.DEFAULT)
        webcam_face_index = int(input("Which face do you want to use? >"))
        webcam_face_index -= 1
        if 0>webcam_face_index or webcam_face_index>=len(webcam_faces):
            print(colors.FAIL + colors.BOLD + "Invalid index" + colors.DEFAULT)
            sys.exit(1)
    else:
        webcam_face_index = 0
    
    logImage = False
    if len(sys.argv) > 1:
        if sys.argv[1] == "-l" or sys.argv[1] == "--log":
            logImage = True
    if not logImage:
        os.remove("webcam.jpg")
    
    webcam_face_encoding = webcam_faces[webcam_face_index]
    results = face_recognition.compare_faces([password_face_encoding], webcam_face_encoding)
    return results[0]

def main():
    print(colors.DONE + colors.BOLD + colors.UNDERLINE + "pyFacialAuthentication\n" + colors.DEFAULT)
    authorized = check_face()
    print(colors.HEADER + colors.BOLD + "Result: " + colors.DEFAULT, end="")
    if authorized:
        print(colors.DONE + colors.BOLD + "Authorized" + colors.DEFAULT)
    else:
        print(colors.FAIL + colors.BOLD + "Unauthorized" + colors.DEFAULT)

if __name__ == "__main__":
    main()