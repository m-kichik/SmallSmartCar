import re


def process_command(command):
    command = command.lower().replace('ё', 'е')
    if 'вперед' in command:
        match = re.search(f'\d*', command)
        distance = match[0] if match else None
        return ['MoveFront', distance]
    if 'назад' in command:
        match = re.search(f'\d*', command)
        distance = match[0] if match else None
        return ['MoveBack', distance]
    if 'право' in command or 'по час' in command:
        match = re.search(f'\d*', command)
        degrees = match[0] if match else None
        return['RotateRight', degrees]
    if 'лево' in command or 'против час' in command:
        match = re.search(f'\d*', command)
        degrees = match[0] if match else None
        return['RotateLeft', degrees]
    if 'фото' in command or 'картин' in command:
        return ['Photo', None]
    if 'детек' in command:
        return ['Detect', None]
    return None


