import os
import sys
sys.path.append(os.path.abspath('/home/jetbot/jetbot'))

import subprocess
import time

import numpy as np
import cv2

from jetbot import Robot
from jetbot import Camera

class SmallCar():
    def __init__(self):
        self.robot = Robot()
        self.camera = Camera.instance()
        self.movements = ['MoveFront', 'MoveBack', 'RotateRight', 'RotateLeft']
        self.movement_time_const = 10
        self.rotate_time_const = 10
        self.photo = ['Photo', 'Detect']

    def execute(self, command, value=None):
        if command in self.movements:
            self.move(command, value)
        elif command in self.photo:
            self.photo(command)

    def move(self, command, value=0.1):
        if command == 'MoveFront':
            self.robot.forward(0.1)
            time.sleep(self.movement_time_const * value)
            self.robot.stop
            return None
        if command == 'MoveBack':
            self.robot.backward(0.1)
            time.sleep(self.movement_time_const * value)
            self.robot.stop
            return None
        if command == 'RotateRight':
            self.robot.right(0.1)
            time.sleep(self.rotate_time_const * value)
            self.robot.stop()
            return None
        if command == 'RotateLeft':
            self.robot.left(0.1)
            time.sleep(self.rotate_time_const * value)
            self.robot.stop()
            return None

    def photo(self, command):
        image = self.camera.value
        image = np.array(image)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_path = os.path.abspath('smallcar/tmp/cam.jpg')
        cv2.imwrite(image_path, image)
        if command == 'Detect':
            subprocess.call([
                'python', 'smallcarbot/tools/detect.py', f'{image_path}',
                '"smallcar/tmp/"', '--model', 'yolov8n.pt'
                ])
        return image_path
