import face_recognition
import cv2


# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

# Load a training pictures and learn how to recognize it.
me_image = face_recognition.load_image_file("me.JPG")
my_face_encoding = face_recognition.face_encodings(me_image, None, 50)[0]

obama_image = face_recognition.load_image_file("obama.jpg")
obama_face_encoding = face_recognition.face_encodings(obama_image, None, 50)[0]

kanchan_image = face_recognition.load_image_file('kanchan.jpg')
kanchan_face_encoding = face_recognition.face_encodings(kanchan_image, None, 50)[0]

known_encodings = [obama_face_encoding, my_face_encoding, kanchan_face_encoding]
in_screen = [False, False, False]
frequency = {'Chandu':0,'Barack':0, 'Kanchan':0}
c = 0
o = 0
k = 0

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(small_frame)
        face_encodings = face_recognition.face_encodings(small_frame, face_locations)

        face_names = []
        if len(face_encodings)==0:
            c+=1
            o+=1
            k+=1
            if c>10:
                in_screen[0] = False
            if o>10:
                in_screen[1] = False
            if k>10:
                in_screen[2] = False
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            match = face_recognition.compare_faces(known_encodings, face_encoding)
            name = "Unknown"

            if match[0]:
                c=0
                name = "Barack"
                if not in_screen[0]:
                    in_screen[0] = True
                    frequency[name] += 1
                    print 'Barack Obama appeared, ' + str(frequency[name]) + (' times' if frequency[name] > 1 else ' time')
            else:
                c+=1
                if c>10:
                    in_screen[0] = False

            if match[1]:
                o=0
                name = "Chandu"
                if not in_screen[1]:
                    in_screen[1] = True
                    frequency[name]+=1
                    print 'Chandu appeared, ' + str(frequency[name]) + (' times' if frequency[name] > 1 else ' time')
            else:
                o+=1
                if o>10:
                    in_screen[1] = False

            if match[2]:
                k=0
                name = "Kanchan"
                if not in_screen[2]:
                    in_screen[2] = True
                    frequency[name] += 1
                    print 'Kanchan Bahirat appeared, ' + str(frequency[name]) + (' times' if frequency[name] > 1 else ' time')
            else:
                k+=1
                if k>10:
                    in_screen[2] = False

            face_names.append(name)
    process_this_frame = not process_this_frame


    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
