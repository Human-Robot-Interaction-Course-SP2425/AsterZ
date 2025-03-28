from utils import *
from chatbot_pipline import *

CAMERA_INDEX = 0  # run list_camera_ports() to choose which camera to use
MIC_INDEX = 0  # run list_audio_devices() to choose which mic to use

model_path = 'models/gesture_recognizer.task'

hand_to_seq = {
    "Open_Palm": "reset",
    "Closed_Fist": "sad",
    "Pointing_Up": "no",
    "Thumb_Up": "happy",
    "Thumb_Down": "fear",
    "ILoveYou": "happy_bounce"
}


handedness_to_seq = {
    "Open_Palm_Left": "azcustom/evilGlareScream",
    "Closed_Fist_Left": "fear_looking_around",
    "Pointing_Up_Left": "anger_cross",
    "Thumb_Up_Left": "happy_head_bobbing",
    "Thumb_Down_Left": "sad_despair",
    "ILoveYou_Left": "happy_daydream",
    "Victory_Left": "fear_faint",

    "Open_Palm_Right": "reset",
    "Closed_Fist_Right": "sad",
    "Pointing_Up_Right": "no",
    "Thumb_Up_Right": "happy",
    "Thumb_Down_Right": "fear",
    "ILoveYou_Right": "happy_bounce",
    "Victory_Right": "fear_anxious"
}
#ILoveYou and Victory are the additional gestures
    # "Victory": "azcustom/evilGlareScream"



# this function runs every time the model detects a gesture
def on_detection(result: GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
    # # GestureRecognizerResult format:
    # # https://ai.google.dev/edge/mediapipe/solutions/vision/gesture_recognizer/python#handle_and_display_results

    # getting the detected gesture name
    gesture_name = result.gestures[0][0].category_name

    # getting the detected gesture handedness (Left or Right)
    gesture_handedness = result.handedness[0][0].category_name 
    print("hand: ", gesture_handedness)

    gesture_hand_combo = gesture_name + "_" +gesture_handedness

    if gesture_hand_combo in handedness_to_seq:  #checking if the gesture name is in the dict
            print("gesture:", gesture_hand_combo, "-> running:", handedness_to_seq[gesture_hand_combo])
            run_seq(handedness_to_seq[gesture_hand_combo])  # running the corresponding sequence
    # displays handtracking
    visualizer(result, output_image)




# # this function runs every time the model detects a gesture
# def on_detection(result: GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
#     # # GestureRecognizerResult format:
#     # # https://ai.google.dev/edge/mediapipe/solutions/vision/gesture_recognizer/python#handle_and_display_results

#     # # getting the detected gesture name
#     # gesture_name = result.gestures[0][0].category_name
#     # #TODO maybe edit this to recognize multiple hands???

#     # if gesture_name in hand_to_seq:  #checking if the gesture name is in the dict
#     #     print("gesture:", gesture_name, "-> running:", hand_to_seq[gesture_name])
#     #     run_seq(hand_to_seq[gesture_name])  # running the corresponding sequence

#     # # displays handtracking
#     # visualizer(result, output_image)

#     # # if you want to add your own custom overlay
#     # # out_frame = cv2.circle(output_image.numpy_view().copy(), (100, 100), 50, (0, 0, 255), 200)
    
#     #TODO test handedness
#         # GestureRecognizerResult format:
#     # https://ai.google.dev/edge/mediapipe/solutions/vision/gesture_recognizer/python#handle_and_display_results

#     # getting the detected gesture name
#     gesture_name = result.gestures[0][0].category_name
#     #TODO maybe edit this to recognize multiple hands???

#     # getting the detected gesture handedness (Left or Right)
#     gesture_handedness = result.handedness[0][0].category_name 
#     print("hand: ", gesture_handedness)

#     gesture_hand_combo = gesture_name + "_" +gesture_handedness
#     # if gesture_name in hand_to_seq:  #checking if the gesture name is in the dict
#     #     print("gesture:", gesture_name, "-> running:", hand_to_seq[gesture_name])
#     #     run_seq(hand_to_seq[gesture_name])  # running the corresponding sequence
#     if gesture_hand_combo in handedness_to_seq:  #checking if the gesture name is in the dict
#             print("gesture:", gesture_hand_combo, "-> running:", handedness_to_seq[gesture_hand_combo])
#             run_seq(handedness_to_seq[gesture_hand_combo])  # running the corresponding sequence
#     # displays handtracking
#     visualizer(result, output_image)


#     # #TODO TEsting multiple hands???
#     # # GestureRecognizerResult format:
#     # # https://ai.google.dev/edge/mediapipe/solutions/vision/gesture_recognizer/python#handle_and_display_results

#     # # getting the detected gesture name
#     # gesture_name1 = result[0].gestures[0][0].category_name
#     # gesture_name2 = result[1].gestures[0][0].category_name
#     # #TODO maybe edit this to recognize multiple hands???

#     # if gesture_name1 in hand_to_seq:  #checking if the gesture name is in the dict
#     #     print("gesture1:", gesture_name1, "-> running:", hand_to_seq[gesture_name1])
#     #     run_seq(hand_to_seq[gesture_name1])  # running the corresponding sequence
#     # if gesture_name2 in hand_to_seq:  #checking if the gesture name is in the dict
#     #         print("gesture2:", gesture_name2, "-> running:", hand_to_seq[gesture_name2])
#     #         run_seq(hand_to_seq[gesture_name2])  # running the corresponding sequence

#     # # displays handtracking
#     # visualizer(result, output_image)

#     # # if you want to add your own custom overlay
#     # # out_frame = cv2.circle(output_image.numpy_view().copy(), (100, 100), 50, (0, 0, 255), 200)



def main():
    init_robot()
    init_model(model_path, on_detection)

    # For webcam input:
    vid = cv2.VideoCapture(CAMERA_INDEX)
    # creating recognizer object
    with GestureRecognizer.create_from_options(model.options) as recognizer:
        # start the camera for recording
        while vid.isOpened():
            # get a frame from the camera
            success, frame = vid.read()
            if not success:
                print("Ignoring empty camera frame.")
                continue  # If loading a video, use 'break' instead of 'continue'.

            # Convert the frame received from OpenCV to a MediaPipe’s Image object.
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)

            # running the model
            recognizer.recognize_async(mp_image, int(vid.get(cv2.CAP_PROP_POS_MSEC)))

            if len(model.out_frame) != 0:
                frame = model.out_frame
            # Display the resulting frame
            cv2.imshow('frame', frame)
            model.out_frame = np.array([])

            # close camera when you press q
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    # After the loop release the cap object
    vid.release()
    # Destroy all the windows
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
