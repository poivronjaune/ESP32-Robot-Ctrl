from machine import Pin, PWM

frequency = 20                  # frequency of PWM signal to motor
Motor1In1 = Pin(26,Pin.OUT)     # This controls motor direction along with In2
Motor1In2 = Pin(27,Pin.OUT)     # same values on In1 and In2 means stop, different value means forward or backwards
Motor1In1.value(0)
Motor1In2.value(0)

Motor2In1 = Pin(25,Pin.OUT)     # This controls motor direction along with In2
Motor2In2 = Pin(33,Pin.OUT)     # same values on In1 and In2 means stop, different value means forward or backwards
Motor2In1.value(0)
Motor2In2.value(0)

Motor1Speed = PWM(Pin(14), frequency)   # Enable pin on motor controls speed through PWM
Motor2Speed = PWM(Pin(32), frequency)    # Enable pin on motor controls speed through PWM

# Forward default speed = 500
def forward(speedLeft = 500, speedRight = 500):
    Motor1In1.value(0)
    Motor1In2.value(1)
    Motor2In1.value(1)
    Motor2In2.value(0)
    Motor1Speed.duty(speedLeft)
    Motor2Speed.duty(speedRight)

# Backward = reverse the In1 and In2 Pins
def backward(speedLeft = 500, speedRight = 500):
    Motor1In1.value(1)
    Motor1In2.value(0)
    Motor2In1.value(0)
    Motor2In2.value(1)
    Motor1Speed.duty(speedLeft)
    Motor2Speed.duty(speedRight)

def stop():
    Motor1In1.value(0)
    Motor1In2.value(0)
    Motor2In1.value(0)
    Motor2In2.value(0)
 
def right(speedLeft = 500, speedRight = 500):
    Motor1In1.value(1)   # Left motor goes backward
    Motor1In2.value(0)
    Motor2In1.value(1)   # Right motor goes forward
    Motor2In2.value(0)
    Motor1Speed.duty(speedLeft)
    Motor2Speed.duty(speedRight)
    
def left(speedLeft = 500, speedRight = 500):
    Motor1In1.value(0)   # Left motor goes forward
    Motor1In2.value(1)
    Motor2In1.value(0)   # Right motor goes backward
    Motor2In2.value(1)
    Motor1Speed.duty(speedLeft)
    Motor2Speed.duty(speedRight)    