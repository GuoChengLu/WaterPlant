import RPi.GPIO as gpio
import time
 
gpio.setmode(gpio.BOARD)
gpio.setwarnings(False)
 
pin = [31, 33, 35, 37]
for i in range(4):
    gpio.setup(pin[i], gpio.OUT)
 
forward_sq = ['0011', '1001', '1100', '0110']
reverse_sq = ['0110', '1100', '1001', '0011']
 
def forward(steps, delay):
    for i in range(steps):
        for step in forward_sq:
            set_motor(step)
            time.sleep(delay)
 
def reverse(steps, delay):
    for i in range(steps):
        for step in reverse_sq:
            set_motor(step)
            time.sleep(delay)
 
def set_motor(step):
    for i in range(4):
        gpio.output(pin[i], step[i] == '1')
 
while True:
    set_motor('0000')
    #forward(180, 0.01)
    reverse(180, 0.01)

