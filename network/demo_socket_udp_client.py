# This file is part of MaixPY
# Copyright (c) sipeed.com
#
# Licensed under the MIT license:
#   http://www.opensource.org/licenses/mit-license.php
#

#network_wiznet5k()

SSID = "Sipeed_2.4G"
PASW = "xxxxxxxx"

def enable_esp32():
    from network_esp32 import wifi
    if wifi.isconnected() == False:
        for _ in range(5):
            try:
                # Running within 3 seconds of power-up can cause an SD load error
                # wifi.reset(is_hard=False)
                wifi.reset(is_hard=True)
                print('try AT connect wifi...')
                wifi.connect(SSID, PASW)
                if wifi.isconnected():
                    break
            except Exception as e:
                print(e)
    print('network state:', wifi.isconnected(), wifi.ifconfig())

#enable_esp32()

# UDP not support enable_espat

def network_wiznet5k():
    from network_wiznet5k import lan
    from machine import SPI
    from Maix import GPIO
    if lan.isconnected() == False:
        WIZNET5K_SPI_SCK = 21
        WIZNET5K_SPI_MOSI = 8
        WIZNET5K_SPI_MISO = 15
        WIZNET5K_SPI_CS = 20
        spi1 = SPI(4, mode=SPI.MODE_MASTER, baudrate=600 * 1000,
                    polarity=0, phase=0, bits=8, firstbit=SPI.MSB, sck=WIZNET5K_SPI_SCK, mosi=WIZNET5K_SPI_MOSI, miso=WIZNET5K_SPI_MISO)
        for _ in range(5):
            try:
                lan.reset(spi1, WIZNET5K_SPI_CS)
                print('try connect lan...')
                if lan.isconnected():
                    break
            except Exception as e:
                print(e)
    print('network state:', lan.isconnected(), lan.ifconfig())

# network_wiznet5k()

import socket

ADDR = ("192.168.0.107", 60000)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(1)

while 1:
    try:
        sock.sendto("hello\n", ADDR)
        data, addr = sock.recvfrom(1024)
    except Exception as e:
        print("receive error:", e)
        continue
    print("addr:", addr, "data:", data)
    time.sleep(2)

sock.close()

'''
>>>
raw REPL; CTRL-B to exit
>OK
network state: True ('192.168.0.186', '255.255.255.0', '192.168.0.1')
addr: ('192.168.0.107', 60000) data: b'HELLO\n'
addr: ('192.168.0.107', 60000) data: b'HELLO\n'
addr: ('192.168.0.107', 60000) data: b'HELLO\n'
'''
