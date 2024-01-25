import streamlit as st
import cv2
import mediapipe as mp

def check_gaze_direction(face_landmarks):
    if 0.42 < face_landmarks.landmark[0].x < 0.62 and 0.40 < face_landmarks.landmark[0].y < 1.6:
        return True
    else:
        return False

def main():
    mal=False
    if not mal:
        mp_face_detection = mp.solutions.face_detection
        face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.3)

        mp_holistic = mp.solutions.holistic
        face_landmarks = mp_holistic.Holistic()

        cap = cv2.VideoCapture(0)

        title=st.title("Proctored Learning")


        saa=st.sidebar.empty()

        # Video stream in sidebar
        st.sidebar.title("Video Stream")
        video_place = st.sidebar.empty()
        warn=st.sidebar.empty()

        question=st.title("")
        options= st.empty()
        answer=st.empty()
        num = 0 
        looked_away=0
        strike=0
        last_looked_away=0
        while cap.isOpened():
            if not mal:
                num+=1
                saa.warning("Time left: "+str(num-last_looked_away)+str(mal)+str(strike))
                question.title("1. What is the time complexity of QuickSort algorithm?")
                options.radio(" " ,("a) O(1)","b) O(n)","c) O(nlogn)","d) O(n^2)"),key=(num/100+0.0001))
                answer.button("Submit",key=num*-1)
                
            
                ret, frame = cap.read()
                if not ret:
                    break

                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                results_detection = face_detection.process(rgb_frame)
                results_landmarks = face_landmarks.process(rgb_frame)

                if results_detection.detections:
                    for detection in results_detection.detections:
                        bboxC = detection.location_data.relative_bounding_box
                        ih, iw, _ = frame.shape
                        bbox = int(bboxC.xmin * iw), int(bboxC.ymin * ih), \
                            int(bboxC.width * iw), int(bboxC.height * ih)
                        cv2.rectangle(frame, bbox, (0, 255, 0), 2)

                if results_landmarks and results_landmarks.face_landmarks:
                    landmarks = results_landmarks.face_landmarks
                    gaze_direction = check_gaze_direction(landmarks)
                    if not gaze_direction:
                        warn.warning("Not looking at screen")
                       
                        if(num-last_looked_away>50):
                            strike+=1
                            last_looked_away=num
                       
                        if strike>2:
                            mal=True
                    else:
                        warn.warning("Looking at screen")
                        last_looked_away=num

                if not results_landmarks.face_landmarks:
                    warn.warning("Face not detected")
                    
                    if(num-last_looked_away>50):
                        strike+=1
                        last_looked_away=num
                       
                 
                    
                    if strike>2:
                        mal=True
               
                video_place.image(frame, channels="BGR")

                num += 1
            else:
                question.header(":white[This attempt has been flagged as malicious due to suspicious activity such as looking away from the screen for too long.\nReattempt the test to continue.]")
                options.empty()
                answer.empty()
                warn.empty()
                video_place.empty()
                st.sidebar.empty()
                st.empty()
                saa.empty()
                title.title(":red[Malicious activity detected!]")
               
               
        cap.release()


if __name__ == "__main__":
    main()
