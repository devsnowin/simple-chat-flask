import random
from string import ascii_uppercase


def generate_unique_code(length, rooms, room_id):
    while True:
        room_id = ""
        for _ in range(length):
            room_id += random.choice(ascii_uppercase)

        if room_id not in rooms:
            break

    return room_id
