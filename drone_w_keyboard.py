from my_keyboard import Keyboard
from djitellopy import tello
import time
import numpy as np
import cv2


class Drone:
    def __init__(self, debug=False):
        self.speed = 50
        self.lr_velocity = 0
        self.fb_velocity = 0
        self.ud_velocity = 0
        self.yaw_velocity = 0

        self.w = 320
        self.h = 240

        # height
        self.p_h = 1
        self.i_h = 0
        self.d_h = 0.5

        # width
        self.p_w = 0.2
        self.i_w = 0
        self.d_w = 1

        # front
        self.p_f = 0.02
        self.i_f = 0
        self.d_f = 0.1

        self.face_area = 3600

        self.follow_w_error = 0
        self.follow_h_error = 0
        self.follow_f_error = 0

        self.is_launched = False
        self.follow = False
        self.record = False

        self.kb = Keyboard()

        self.device = tello.Tello()
        self.device.connect()

        self.get_battery()
        self.device.streamon()
        self.frameReader = self.device.get_frame_read()

        self.face_cascade = None
        self.video_writer = None

        self.debug = debug

        self.end = False

    def get_battery(self):
        print(f'battery: {self.device.get_battery()}')

    def get_speed(self):
        print(f'speed: {self.speed}\n'
              f'p_h: {self.p_h}\n'
              f'd_h: {self.d_h}\n'
              f'p_w: {self.p_w}\n'
              f'd_w: {self.d_w}'
              f'p_f: {self.p_f}\n'
              f'd_f: {self.d_f}'
              )

    def get_keys(self):

        self.kb.get_all_keys()

        if self.kb.get_key('SPACE'):

            if self.is_launched:
                self.device.land()
                self.is_launched = False
            else:
                self.device.takeoff()
                self.is_launched = True

            while self.kb.get_key('SPACE'):
                time.sleep(0.1)
                self.kb.get_all_keys()
            return

        if self.kb.get_key('b'):
            self.get_battery()
            while self.kb.get_key('b'):
                time.sleep(0.1)
                self.kb.get_all_keys()

        if self.kb.get_key('v'):
            self.get_speed()
            while self.kb.get_key('v'):
                time.sleep(0.1)
                self.kb.get_all_keys()

        if self.kb.get_key('f'):
            self.follow = ~self.follow
            # self.speed = 30
            self.face_cascade = cv2.CascadeClassifier('casc/haarcascade_frontalface_alt.xml')
            while self.kb.get_key('f'):
                time.sleep(0.1)
                self.kb.get_all_keys()

        if self.kb.get_key('q'):
            if self.video_writer is not None:
                self.video_writer.release()
            self.device.end()
            while self.kb.get_key('q'):
                time.sleep(0.1)
                self.kb.get_all_keys()
            self.end = True
            return

        if self.kb.get_key('r'):
            if self.video_writer is None:
                fourcc = cv2.VideoWriter_fourcc(*'XVID')
                self.video_writer = cv2.VideoWriter('output.avi', fourcc, 20.0, (self.w, self.h))
            self.record = ~self.record
            while self.kb.get_key('r'):
                time.sleep(0.1)
                self.kb.get_all_keys()

        if self.kb.get_key('a'):
            self.lr_velocity = -self.speed
        elif self.kb.get_key('d'):
            self.lr_velocity = self.speed
        elif ~self.follow:
            self.lr_velocity = 0

        if self.kb.get_key('w'):
            self.fb_velocity = self.speed
        elif self.kb.get_key('s'):
            self.fb_velocity = -self.speed
        elif ~self.follow:
            self.fb_velocity = 0

        if self.kb.get_key('UP'):
            self.ud_velocity = self.speed
        elif self.kb.get_key('DOWN'):
            self.ud_velocity = -self.speed
        elif ~self.follow:
            self.ud_velocity = 0

        if self.kb.get_key('LEFT'):
            self.yaw_velocity = -self.speed
        elif self.kb.get_key('RIGHT'):
            self.yaw_velocity = self.speed
        elif ~self.follow:
            self.yaw_velocity = 0

        if self.kb.get_key('LSHIFT'):
            self.speed += 10
            while self.kb.get_key('LSHIFT'):
                time.sleep(0.1)
                self.kb.get_all_keys()
            if self.speed > 100:
                self.speed = 100
        elif self.kb.get_key('LCTRL'):
            self.speed -= 10
            while self.kb.get_key('LCTRL'):
                time.sleep(0.1)
                self.kb.get_all_keys()
            if self.speed < 10:
                self.speed = 10

        if self.kb.get_key('F1'):
            self.d_f += 0.01
            while self.kb.get_key('F1'):
                time.sleep(0.1)
                self.kb.get_all_keys()
        elif self.kb.get_key('F2'):
            self.d_f -= 0.01
            while self.kb.get_key('F2'):
                time.sleep(0.1)
                self.kb.get_all_keys()

    def follow_face(self, img):

        if self.debug:
            cv2.circle(img, (self.w // 2, self.h // 2), 4, (255, 0, 0), -1)

        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(img_gray, minNeighbors=2)

        my_face_listC = []
        my_face_list_area = []
        my_face_list = []

        for (x, y, w, h) in faces:
            center_x = x + w // 2
            center_y = y + h // 2
            my_face_list_area.append(h * w)
            my_face_listC.append((center_x, center_y))
            my_face_list.append((x, y, w, h))

            if self.debug:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.circle(img, (center_x, center_y), 4, (0, 255, 0), -1)
                cv2.putText(img, f'S = {my_face_list_area[-1]}', (x + w, y), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 1)

        if len(my_face_list_area) != 0:
            area = max(my_face_list_area)
            i = my_face_list_area.index(area)
            center_x, center_y = my_face_listC[i]
            x, y, w, h = my_face_list[i]
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)

            f_error = -(area - self.face_area)

            self.fb_velocity = f_error * self.p_f + (f_error - self.follow_f_error) * self.d_f
            self.fb_velocity = int(np.clip(self.fb_velocity, -self.speed, self.speed))

            w_error = center_x - self.w // 2
            h_error = -(center_y - (self.h // 2))

            self.lr_velocity = w_error * self.p_w + (w_error - self.follow_w_error) * self.d_w
            self.lr_velocity = int(np.clip(self.lr_velocity, -self.speed, self.speed))

            self.ud_velocity = h_error * self.p_h + (h_error - self.follow_h_error) * self.d_h
            self.ud_velocity = int(np.clip(self.ud_velocity, -self.speed, self.speed))

            self.follow_w_error = w_error
            self.follow_h_error = h_error
            self.follow_f_error = f_error

            self.yaw_velocity = 0
            # self.lr_velocity = 0
            # self.ud_velocity = 0

        else:
            self.lr_velocity = 0
            self.fb_velocity = 0
            self.ud_velocity = 0
            self.yaw_velocity = 0

    def send_control(self):

        if self.is_launched:
            self.device.send_rc_control(
                left_right_velocity=self.lr_velocity,
                forward_backward_velocity=self.fb_velocity,
                up_down_velocity=self.ud_velocity,
                yaw_velocity=self.yaw_velocity
            )

    def print_info(self):
        print(f'forward_backward_velocity={self.fb_velocity}\n'
              f'left_right_velocity={self.lr_velocity}\n'
              f'up_down_velocity={self.ud_velocity}\n'
              f'yaw_velocity={self.yaw_velocity}')
