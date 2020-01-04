#coding=utf-8
import RPi.GPIO as GPIO
import time
import Adafruit_DHT

#土壤濕度監測
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7,GPIO.IN)

#溫濕度pin腳
GPIO_PIN = 14

#伺服馬達
CONTROL_PIN = 11
PWM_FREQ = 50
STEP=90
GPIO.setup(CONTROL_PIN, GPIO.OUT)
pwm = GPIO.PWM(CONTROL_PIN, PWM_FREQ)
pwm.start(0)

#伺服馬達角度
def angle_to_duty_cycle(angle=0):
    duty_cycle = (0.05 * PWM_FREQ) + (0.19 * PWM_FREQ * angle / 180)
    return duty_cycle


try:
    file = open("soildata.txt", "w")
    print('按下 Ctrl-C 可停止程式')
    watering = 0
    nowatering = 0
    counting = 0
    while True:

        #時間
        ts = time.localtime(time.time())
        timestr = str(ts.tm_year)+"/"+str(ts.tm_mon)+"/"+str(ts.tm_mday)+" "+str(ts.tm_hour)+":"+str(ts.tm_min)+":"+str(ts.tm_sec)
        h, t = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, GPIO_PIN)
        if counting == 24:
            file.seek(0)
            file.truncate()
            counting = 0
        #土壤監測
        if GPIO.input(7) == False:
            print timestr
            print "土壤濕度足夠:)"
            file.write(timestr +" "+'" "'+" ")
            if nowatering == 0:
                for angle in range(90, -1, -STEP):
                    dc = angle_to_duty_cycle(angle)
                    #print('角度={: >3}, 工作週期={:.2f}'.format(angle, dc))
                    pwm.ChangeDutyCycle(dc)
                    time.sleep(0.5)
            nowatering = 1
            watering = 0
        elif GPIO.input(7) == True:
            print timestr
            print "土壤濕度不夠請澆水><"
            file.write(timestr +" "+"watering"+ " ")
            if (watering == 0 and t <= 28):
                for angle in range(0, 91, STEP):
                    dc = angle_to_duty_cycle(angle)
                    pwm.ChangeDutyCycle(dc)
                    #print('角度={: >3}, 工作週期={:.2f}'.format(angle, dc))
                    time.sleep(0.5)
            elif t>28:
                print "由於氣溫過高所以暫停澆水"
            watering = 1
            nowatering = 0


        if h is not None and t is not None:
            print('溫度={0:0.1f}度C 空氣濕度={1:0.1f}%'.format(t, h))
            file.write('{0:0.1f}°C {1:0.1f}%'.format(t, h) + "\n")
        else:
            print('讀取失敗')
            file.write("讀取失敗"+ "\n")
        counting=counting+1
        time.sleep(0.5)
except KeyboardInterrupt:
    print('關閉程式')
    pwm.stop()
    GPIO.cleanup()
    file.close()
