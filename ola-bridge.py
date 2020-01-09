#!/usr/bin/env python2

from ola.ClientWrapper import ClientWrapper

import serial
import time
import binascii


# Slightly ridiculous software to read OLA messages and talk to a Zoom H6 remote
# so that it can be controlled with QLC+ or any lighting console... yup, haha!

# WARNING! Again, this is ridiculous. I mean, it works fine, but it's not exactly been poured over

# It takes 8 hardcoded (see above!) channels of DMX and interprets them as:
#   1 - Left
#   2 - Right
#   3 - Channel 1
#   4 - Channel 2
#   5 - Channel 3
#   6 - Channel 4
#   7 - Play
#   8 - Record

# For the keypad buttons:
#     0 - 100 = Off
#   101 - 150 = Red
#   151 - 200 = Yellow
#   201 - 250 = Green
#   251 - 100 = Off

# For the transport controls:
#     0 - 100 = Off
#   101 - 250 = Green
#   251 - 255 = Off


universe = 1

s = serial.Serial('/dev/ttyUSB0')
s.baudrate = 2400
s.write(bytearray([0b10000010]))
time.sleep(0.5)
last_tx_data = bytearray([0b10000100, 0b00000000, 0b00000000])


def NewData(data):
    init_byte = bytearray([0b10000100])
    data_bytes = bytearray([0b00000000, 0b00000000])

    clear = bytearray([0b00000000, 0b00000000])
    play = bytearray([0b00000000, 0b00000001])
    rec = bytearray([0b00000001, 0b00000000])

    # r = record = red
    rl = bytearray([0b00100000, 0b00000000])
    rr = bytearray([0b00001000, 0b00000000])
    r1 = bytearray([0b00000010, 0b00000000])
    r2 = bytearray([0b00000000, 0b00100000])
    r3 = bytearray([0b00000000, 0b00001000])
    r4 = bytearray([0b00000000, 0b00000010])

    # s = solo = yellow
    sl = bytearray([0b01100000, 0b00000000])
    sr = bytearray([0b00011000, 0b00000000])
    s1 = bytearray([0b00000110, 0b00000000])
    s2 = bytearray([0b00000000, 0b01100000])
    s3 = bytearray([0b00000000, 0b00011000])
    s4 = bytearray([0b00000000, 0b00000110])

    # p = play = green
    pl = bytearray([0b01000000, 0b00000000])
    pr = bytearray([0b00010000, 0b00000000])
    p1 = bytearray([0b00000100, 0b00000000])
    p2 = bytearray([0b00000000, 0b01000000])
    p3 = bytearray([0b00000000, 0b00010000])
    p4 = bytearray([0b00000000, 0b00000100])

    
    data_list = []

    if data[0] > 100 and data[0] < 151:
        data_list.append(rl)
    elif data[0] > 150 and data[0] < 201:
        data_list.append(sl)
    elif data[0] > 200 and data[0] < 251:
        data_list.append(pl)

    if data[1] > 100 and data[1] < 151:
        data_list.append(rr)
    elif data[1] > 150 and data[1] < 201:
        data_list.append(sr)
    elif data[1] > 200 and data[1] < 251:
        data_list.append(pr)

    if data[2] > 100 and data[2] < 151:
        data_list.append(r1)
    elif data[2] > 150 and data[2] < 201:
        data_list.append(s1)
    elif data[2] > 200 and data[2] < 251:
        data_list.append(p1)

    if data[3] > 100 and data[3] < 151:
        data_list.append(r2)
    elif data[3] > 150 and data[3] < 201:
        data_list.append(s2)
    elif data[3] > 200 and data[3] < 251:
        data_list.append(p2)

    if data[4] > 100 and data[4] < 151:
        data_list.append(r3)
    elif data[4] > 150 and data[4] < 201:
        data_list.append(s3)
    elif data[4] > 200 and data[4] < 251:
        data_list.append(p3)

    if data[5] > 100 and data[5] < 151:
        data_list.append(r4)
    elif data[5] > 150 and data[5] < 201:
        data_list.append(s4)
    elif data[5] > 200 and data[5] < 251:
        data_list.append(p4)

    if data[6] > 100 and data[6] < 251:
        data_list.append(play)

    if data[7] > 100 and data[7] < 251:
        data_list.append(rec)

    for bytes in data_list:
        data_bytes = bytearray([data_bytes[0] | bytes[0]]) + bytearray([data_bytes[1] | bytes[1]])

    tx_data = init_byte + data_bytes

    global last_tx_data
    if tx_data != last_tx_data:
        print 'Writing data', binascii.hexlify(tx_data)
        s.write(tx_data)
        last_tx_data = tx_data


wrapper = ClientWrapper()
client = wrapper.Client()
client.RegisterUniverse(universe, client.REGISTER, NewData)
wrapper.Run()
