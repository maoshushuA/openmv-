from pyb import Pin, Timer
inverse_left=False  #change it to True to inverse left wheel
inverse_right=False #change it to True to inverse right wheel

ain1 =  Pin('P0', Pin.OUT_PP)
ain2 =  Pin('P1', Pin.OUT_PP)
bin1 =  Pin('P2', Pin.OUT_PP)
bin2 =  Pin('P3', Pin.OUT_PP)
E = Pin('P4',Pin.OUT_PP)
E.high()
ain1.low()
ain2.low()
bin1.low()
bin2.low()

pwma = Pin('P7')
pwmb = Pin('P8')
tim = Timer(4, freq=1000)
ch1 = tim.channel(1, Timer.PWM, pin=pwma)
ch2 = tim.channel(2, Timer.PWM, pin=pwmb)
ch1.pulse_width_percent(0)
ch2.pulse_width_percent(0)

def run(left_speed, right_speed):
    if inverse_left==True:
        left_speed=(-left_speed)
    if inverse_right==True:
        right_speed=(-right_speed)

    if left_speed < 0:
        ain1.low()
        ain2.high()
    else:
        ain1.high()
        ain2.low()
    ch1.pulse_width_percent(abs(left_speed))

    if right_speed < 0:
        bin1.low()
        bin2.high()
    else:
        bin1.high()
        bin2.low()
    ch2.pulse_width_percent(abs(right_speed))
