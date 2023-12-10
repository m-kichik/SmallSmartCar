from argparse import ArgumentParser
import os
import sys
import subprocess
import time

sys.path.append(os.path.abspath("/home/jetbot/jetbot"))
from jetbot import Robot

robot = Robot()
movement_time_const = 50
rotate_time_const = 10


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("command")
    parser.add_argument("value", type=float)
    return parser.parse_args()


def move(command, value=0.1):
    if command == "MoveFront":
        robot.forward(0.1)
        time.sleep(movement_time_const * value)
        robot.stop()
        return None
    if command == "MoveBack":
        robot.backward(0.1)
        time.sleep(movement_time_const * value)
        robot.stop()
        return None
    if command == "RotateRight":
        robot.right(0.1)
        time.sleep(rotate_time_const * value)
        robot.stop()
        return None
    if command == "RotateLeft":
        robot.left(0.1)
        time.sleep(rotate_time_const * value)
        robot.stop()
        return None


def main():
    args = parse_args()
    move(args.command, args.value)


if __name__ == "__main__":
    main()
