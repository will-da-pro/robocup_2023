import gpiozero

class driveBase():
    def __init__(self, port1: int, port2: int, port3: int, port4: int) -> None:
        gpiozero.setmode(gpiozero.BOARD)
        self.lForwards = gpiozero.PWMOutputDevice(port1)
        self.rForwards = gpiozero.PWMOutputDevice(port2)
        self.lBackwards = gpiozero.PWMOutputDevice(port3)
        self.rBackwards = gpiozero.PWMOutputDevice(port4)
    def drive(self, speed, turnSpeed) -> None:
        self.stop()

        lSpeed = (abs(speed) + turnSpeed) / 1000
        rSpeed = (abs(speed) - turnSpeed) / 1000

        if lSpeed > 1:
            lSpeed = 1
        if rSpeed > 1:
            rSpeed = 1

        if speed >= 0:
            self.lForwards.value = lSpeed
            self.rForwards.value = rSpeed

            self.lForwards.on()
            self.rForwards.on()
        else:
            self.lBackwards.value = lSpeed
            self.rBackwards.value = rSpeed

            self.lBackwards.on()
            self.rBackwards.on()
    def stop(self) -> None:
        self.lForwards.off()
        self.rForwards.off()
        self.lBackwards.off()
        self.rBackwards.off()