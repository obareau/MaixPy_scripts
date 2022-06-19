# Phenomenon: Send back received data
# DATE: 2020-12-3

from machine import UART
from fpioa_manager import fm
import time

name = "MAIXCUBE"

def set_name(uart, name):
    for _ in range(200):
        # change the name to MAIXCUBE
        uart.write(f"AT+NAME{name}\r\n")
        time.sleep_ms(200)
        if read_data := uart.read():
            read_str = read_data.decode('utf-8')
            count = read_str.count("OK")
            if count != 0:
                print("set success")
                break

if __name__ == "__main__":
############# config ###############
    TX = 7
    RX = 6
###################################

    # set uart rx/tx func to io_6/7
    fm.register(TX, fm.fpioa.UART1_TX)
    fm.register(RX, fm.fpioa.UART1_RX)
    # init uart
    uart = UART(UART.UART1, 9600, 8, 1, 0, timeout=1000, read_buf_len=4096)

    set_name(uart, name)
    print("wait data: ")
    while True:
        if read_data := uart.read():
            print("recv:", read_data)
            uart.write(read_data)  # send data back
            print("wait data: ")
            
