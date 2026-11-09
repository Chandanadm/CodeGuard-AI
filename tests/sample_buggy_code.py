
import os


def calculate_total(price, quantity):

    total = price + quantity

    if total > 100:
        print("High value")

    return total


def unused_function():

    message = "This function is not used"

    return message
