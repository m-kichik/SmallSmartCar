import re


def process_command(command):
    command = command.lower().replace('ё', 'е')
    if 'вперед' in command:
        match = re.search(r'\d+', command)
        distance = int(match[0]) if match else None
        return ['MoveFront', distance], "вперёд"
    if 'назад' in command:
        match = re.search(r'\d+', command)
        distance = int(match[0]) if match else None
        return ['MoveBack', distance], "назад"
    if 'право' in command or 'по час' in command:
        match = re.search(r'\d+', command)
        degrees = int(match[0]) if match else None
        return['RotateRight', degrees], "поворот направо"
    if 'лево' in command or 'против час' in command:
        match = re.search(r'\d+', command)
        degrees = int(match[0]) if match else None
        return['RotateLeft', degrees], "поворот налево"
    if 'фото' in command or 'картин' in command:
        return ['Photo', None], "фотография"
    if 'детек' in command:
        return ['Detect', None], "детекция"
    return None


