# -*- coding: utf-8 -*-
"""
RPi Alkalinity
Version: v0.81 (Beta)
Licensed under {License info} for general use with attribution.
For works using this code please cite:
    Sandborn, D.E., Minor E.C., Hill, C. (2022)
"""
import numpy as np
import time
import sys


def say_hello():
    print("  _____  _____ _               _ _         _ _       _ _         \n |  __ \|  __ (_)        /\   | | |       | (_)     (_) |        \n | |__) | |__) | ______ /  \  | | | ____ _| |_ _ __  _| |_ _   _ \n |  _  /|  ___/ |______/ /\ \ | | |/ / _` | | | `_ \| | __| | | |\n | | \ \| |   | |     / ____ \| |   < (_| | | | | | | | |_| |_| |\n |_|  \_\_|   |_|    /_/    \_\_|_|\_\__,_|_|_|_| |_|_|\__|\__, |\n                                                            __/ |\n                                                (C)2021 des|___/ \n                                                           ")
    print("Welcome to RPi-Alkalinity.\nBeta Build 0.8")
    message = "RPi-Alkalinity: Water Alkalinity determined via low-cost and \nopen-source technologies.  Created by Sandborn, D.E., Minor E.C., Hill, C. \nat the Large Lakes Observatory and University of Minnesota Duluth.\n"
    print(message)
    tech = "This program was written to accompany an instrument built by the \nauthors which collects EMF and temperature readings from an acidimetric \ntitration of a water sample.  pH/EMF readings were collected with a Metrohm Ecotrode \nand temperature readings with a DS18B20 thermistor.  This instrument was built \nto operate in a Raspberry Pi (model 3B) environment supplemented by a MCC128 \nDAQ HAT unit and custom amplification circuitry.\n"
    print(tech)
    contact = "This program is freely available on Github at \nwww.github.com/d-sandborn/RPi-Alkalinity.  Questions can be addressed to sandb425@umn.edu.  "
    print(contact)


def chess():
    print("Greetings Professor Falken.  Would you like to play a game?")
    response = input("--> ")
    if "war" in response:
        print("Wouldn't you prefer a good game of chess?")


def countdown(minutes):
    seconds_list = np.flip(np.linspace(0, minutes*60-1, minutes*60))
    for i in seconds_list:
        sys.stdout.write('\r'+"Time left: " + str(int(i)) + " seconds")
        time.sleep(1)
