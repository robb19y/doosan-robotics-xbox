from inputs import get_gamepad
import math
import threading
import time
import socket

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the robot is listening
robot_address = ('192.168.137.50', 9225)
sock.connect(robot_address)


class XboxController(object):
    MAX_TRIG_VAL = math.pow(2, 8)
    MAX_JOY_VAL = math.pow(2, 15)

    def __init__(self):

        self.left = 0
        self.up = 0
        self.zoom = 0
        self.speed = 0
        self.r = 0
        self.fixed = 0
        self.magic = 0

        self._monitor_thread = threading.Thread(target=self.monitor_controller, args=())
        self._monitor_thread.daemon = True
        self._monitor_thread.start()

    def monitor_controller(self):
        while True:

            events = get_gamepad()
            for event in events:
                print(event.code+" "+str(event.state))
                if event.code == 'ABS_HAT0Y':
                    if self.left is not event.state:
                        if event.state > 0:
                            sock.sendall(b"down()")
                        elif event.state < 0:
                            sock.sendall(b"up()")
                        else:
                            sock.sendall(b"stop_motion()")

                    self.left = event.state

                elif event.code == 'ABS_HAT0X':
                    if self.up is not event.state:
                        if event.state > 0:
                            sock.sendall(b"right()")
                        elif event.state < 0:
                            sock.sendall(b"left()")
                        else:
                            sock.sendall(b"stop_motion()")

                    self.up = event.state

                elif event.code == 'BTN_TR':
                    if self.zoom is not event.state:
                        if event.state > 0:
                            sock.sendall(b"t_decrease()")
                        else:
                            sock.sendall(b"stop_motion()")

                    self.zoom = event.state

                elif event.code == 'BTN_TL':
                    if self.zoom is not event.state:
                        if event.state > 0:
                            sock.sendall(b"t_increase()")
                        else:
                            sock.sendall(b"stop_motion()")

                    self.zoom = event.state

                elif event.code == 'ABS_Z':
                    if self.r is not int(event.state/200):
                        if int(event.state/200) > 0:
                            sock.sendall(b"r_decrease()")
                        else:
                            sock.sendall(b"stop_motion()")

                    self.r = int(event.state/200)

                elif event.code == 'ABS_RZ':
                    if self.r is not int(event.state/200):
                        if int(event.state/200) > 0:
                            sock.sendall(b"r_increase()")
                        else:
                            sock.sendall(b"stop_motion()")

                    self.r = int(event.state/200)

                elif event.code == 'BTN_EAST':
                    if self.zoom is not event.state:
                        if event.state > 0:
                            sock.sendall(b"zoom_in()")
                        else:
                            sock.sendall(b"stop_motion()")

                    self.zoom = event.state

                elif event.code == 'BTN_SOUTH':
                    if self.zoom is not event.state:
                        if event.state > 0:
                            sock.sendall(b"zoom_out()")
                        else:
                            sock.sendall(b"stop_motion()")

                    self.zoom = event.state

                elif event.code == 'BTN_SELECT':
                    if self.fixed is not event.state:
                        if event.state > 0:
                            sock.sendall(b"toggle_fixed_position()")
                        else:
                            sock.sendall(b"stop_motion()")

                    self.fixed = event.state

                elif event.code == 'BTN_NORTH':
                    if event.state > 0:
                        sock.sendall(b"increase_speed()")

                    self.speed = event.state

                elif event.code == 'BTN_WEST':
                    if event.state > 0:
                        sock.sendall(b"decrease_speed()")

                    self.speed = event.state

                elif event.code == 'BTN_START':
                    if self.magic is not event.state:
                        if event.state > 0:
                            sock.sendall(b"crazy_zoom()")
                    self.magic = event.state


if __name__ == '__main__':
    joy = XboxController()
    while True:
        time.sleep(10)