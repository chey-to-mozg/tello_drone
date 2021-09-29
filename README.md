## This repository contain code to control the Tello drone

The repository contains auxiliary code `my_keyboard.py`. In this code `pygame` library was used to handle keyboard events.

<strong> !!! Because of `pygame` library, you need to set focus on pygame window when it started, to send commands from the keyboard.</strong>

Using `get_all_keys` we update current state of keyboard events, after that using `get_key` with a key name it will return True or False value depends on a key is pressed or not.

### `drone_w_keyboard.py` describes main class, which contain comands to controll drone. 

`get_battery` method will print to console current battery level.

`get_speed` method will print to console current speed, which was set and all coefficients for autonomous control (coefficints for PID controller)

`get_keys` will update drone parameters depends on pressed buttons. List of all buttons:
- `SPACE` -- will send command to drone to take off if it on ground, will land otherwise;
- `b` -- will call `get_battery` method;
- `v` -- will call `get_speed` method;
- `f` -- will switch 'follow face' mode to On\Off. In this mode, you can still use the keyboard to interrupt autonomous control;
- `q` -- will stop drone control and send command to turn off all streams on the drone. Will land if it is in the air;
- `r` -- will start video recording. By using this button again it will set video writing on pause (only one video by one flight); 
- `a` -- will set current speed to move left;
- `d` -- will set current speed to move right;
- `w` -- will set current speed to move forward;
- `s` -- will set current speed to move backward;
- `UP`(↑) -- will set current speed to move up;
- `DOWN`(↓) -- will set current speed to move down;
- `LEFT`(←) -- will set current speed to turn left;
- `RIGHT`(→) -- will set current speed to turn right;
- `LSHIFT`(left shift) -- will increase current speed (upper bound is set);
- `LCTRL`(left ctrl) -- will decrease current speed (lower bound is set);

`follow_face` method is the main algorithm to detect face and set necessary speed to move the drone so that the face is in the center of the image. The closest face will be chosen. Stays in place if faces are not detected;

`send_control` will send speed parameters to the drone.  
<strong>Pressed keys will send nothing, they just set speed for `send_comand` method</strong>;

`print_info` method will print current left\rigt, forward\backward, up\down, and yaw velocities;

### `main.py` contains the code to launch and control the drone.

1. You need to connect to your drone using WIFI. 
2. Simply run `main.py`
3. If you recorded the video, you can find it in the directory with `main.py` with name `output.avi`

By default it will turn on the video stream.
