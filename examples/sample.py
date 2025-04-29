import os
import sys

def unused_function():
    print("I am never called!")

def used_function(x):
    return x * 2

def plus_one(x):
    return x + 1

result = used_function(5)
