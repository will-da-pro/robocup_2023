import gpiozero
from time import sleep

class driveBase():
    def __init__(self, port1: int, port2: int) -> None:
        gpiozero.setmode(gpiozero.BOARD)
        self.lMotor = gpiozero.PWMOutputDevice(port1, True, 0)
        self.rMotor = gpiozero.PWMOutputDevice(port2, True, 0)

    def drive(self, speed: int, turnSpeed: float=0) -> None:
        """
        Makes the robot drive

        :param int speed:
          Controls the speed at which to drive at. choose a number between -1000 and 1000.

        :param float turnSpeed:
          A number that controls the speed at which to turn. negative is left, positive is right. Default value is zero.
        """
        lSpeed = (abs(speed) + turnSpeed) / 1000
        rSpeed = (abs(speed) - turnSpeed) / 1000

        if lSpeed > 1:
            lSpeed = 1
        if rSpeed > 1:
            rSpeed = 1

        self.lMotor.value = lSpeed
        self.rMotor.value = rSpeed

        self.lMotor.on()
        self.rMotor.on()

    def stop(self) -> None:
        self.lMotor.off()
        self.rMotor.off()

    def straight(self, distance: float, speed: int) -> None:
        self.stop()

        self.lMotor.value = speed / 1000
        self.rMotor.value = speed / 1000

        self.lMotor.on()
        self.rMotor.on()

        sleep(distance)

        self.stop()
