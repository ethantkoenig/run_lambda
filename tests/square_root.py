"""
A dummy lambda function for testing
"""

import math


def handle(event, context):
    return math.sqrt(event["number"])
