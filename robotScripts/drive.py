import gpiozero
from time import sleep

class driveBase():
    def __init__(self, port1: int, port2: int, port3: int, port4) -> None:
        self.lMotor = gpiozero.Motor(port1, port3, pwm=True)
        self.rMotor = gpiozero.Motor(port2, port4, pwm=True)

    def drive(self, speed: int, turnSpeed: float=0) -> None:
        """
        Makes the robot drive

        :param int speed:
          Controls the speed at which to drive at. choose a number between -1000 and 1000.

        :param float turnSpeed:
          A number that controls the speed at which to turn. negative is left, positive is right. Default value is zero.
        """

        lSpeed = (speed + turnSpeed) / 1000
        rSpeed = (speed - turnSpeed) / 1000

        if lSpeed > 1:
            lSpeed = 1
        if rSpeed > 1:
            rSpeed = 1

        if lSpeed >= 0:
            self.lMotor.forward(lSpeed)
        else:
            self.lMotor.backward(abs(lSpeed))
        if rSpeed >= 0:
            self.rMotor.forward(rSpeed)
        else:
            self.rMotor.backward(abs(rSpeed))

    def stop(self) -> None:
        self.lMotor.stop()
        self.rMotor.stop()

    def straight(self, distance: float, speed: int) -> None:
        self.stop()

        self.lMotor.forward(speed / 1000)
        self.rMotor.forward(speed / 1000)

        sleep(distance)

        self.stop()
