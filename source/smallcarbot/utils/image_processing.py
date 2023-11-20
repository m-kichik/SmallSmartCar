import subprocess

def detect(image_path):
    subprocess.call([
        'python', 'smallcarbot/utils/detect.py', f'{image_path}',
        '"smallcarbot/tmp/"', '--model', 'yolov8n.pt'
        ])
