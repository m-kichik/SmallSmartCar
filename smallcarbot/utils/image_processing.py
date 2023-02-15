import subprocess

def detect(image_path):
    subprocess.call([
        'python', 'smallcarbot/tools/detect.py', f'{image_path}',
        '"smallcarbot/tmp/"', '--model', 'yolov8n.pt'
        ])
