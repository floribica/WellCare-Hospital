import random


def generate_random_string(length):
    chars = "0123456789ABCDEFGHIJKELNOPKQSTUVYZWXZabcdefhijklmnopqrstuvwxz!@?"
    return ''.join(random.choice(chars) for _ in range(length))
