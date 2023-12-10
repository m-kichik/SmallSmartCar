import os
import sys
import subprocess
import time


class SmallCar:
    def __init__(self):
        self.movements = ["MoveFront", "MoveBack", "RotateRight", "RotateLeft"]
        self.movement_time_const = 50
        self.rotate_time_const = 10
        self.photo = ["Photo", "Detect"]

    def execute(self, command):
        if command[0] in self.movements:
            value = 0.1 if command[1] is None else command[1]
            subprocess.call(
                [
                    "/usr/bin/python3.6",
                    "smallcar/move.py",
                    command[0],
                    str(value),
                ]
            )
            return {"move_command": True, "status": "SUCCESS"}

        elif command[0] in self.photo:
            print("IN PHOTO")
            return {
                "move_command": False,
                "image_path": None,
                "status": "Disabled function :(",
            }

            # impath = os.path.abspath("smallcarbot/tmp/cam.jpg")
            # subprocess.call(
            #     [
            #         "/usr/bin/python3.6",
            #         "smallcar/photo.py",
            #         command[0],
            #         impath,
            #     ]
            # )

            # return impath

        return {"move_command": False, "image_path": None, "status": "Unknown command"}
