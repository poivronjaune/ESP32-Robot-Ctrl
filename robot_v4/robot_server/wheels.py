from machine import Pin, PWM

frequency = 20                  # frequency of PWM signal to motor
Motor1In1 = Pin(13,Pin.OUT)     # This controls motor direction along with In2
Motor1In2 = Pin(15,Pin.OUT)     # same values on In1 and In2 means stop, different value means forward or backwards
Motor1In1.value(0)
Motor1In2.value(0)

Motor2In1 = Pin(14,Pin.OUT)     # This controls motor direction along with In2
Motor2In2 = Pin(2,Pin.OUT)      # same values on In1 and In2 means stop, different value means forward or backwards
Motor2In1.value(0)
Motor2In2.value(0)

Motor1Speed = PWM(Pin(12), frequency)   # Enable pin on motor controls speed through PWM
Motor2Speed = PWM(Pin(4), frequency)    # Enable pin on motor controls speed through PWM

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
    
