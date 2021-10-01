import cv2
from drone_w_keyboard import Drone

if __name__ == '__main__':
    drone = Drone()

    while True:

        frame = drone.frameReader.frame
        frame = cv2.resize(frame, (drone.w, drone.h))

        if drone.reverse_frame:
            frame = frame[50:, :]
            frame = cv2.cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame = cv2.flip(frame, -1)
        if drone.follow:
            drone.follow_face(frame)

        drone.get_keys()

        if drone.end:
            print("end of the program")
            cv2.destroyAllWindows()
            break

        drone.send_control()

        if drone.record:
            print(f'{frame.shape}')
            drone.video_writer.write(frame)
            cv2.circle(frame, (10, 10), 7, (0, 0, 255), -1)

        cv2.imshow('image', frame)

        cv2.waitKey(1)