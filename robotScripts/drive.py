import gpiozero
from time import process_time

class driveBase():
    def __init__(self, port1: int, port2: int, port3: int, port4: int, defaultSpeed=500) -> None:
        """
        A class for all your robot driving needs. Use these functions for any movement.

        :param int port1:
        The GPIO pin to use for forward input in the left motor.

        :param int port2:
        The GPIO pin to use for forward input in the right motor.

        :param int port3:
        The GPIO pin to use for backward input in the left motor.

        :param int port4:
        The GPIO pin to use for backward input in the right motor.
        """

        self.lMotor = gpiozero.Motor(port1, port3, pwm=True)
        self.rMotor = gpiozero.Motor(port2, port4, pwm=True)

        self.defaultSpeed = defaultSpeed

    def drive(self, speed: int = None, turnSpeed: float = 0) -> None:
        """
        Makes the robot drive

        :param int speed:
          Controls the speed at which to drive at. choose a number between -1000 and 1000.

        :param float turnSpeed:
          A number that controls the speed at which to turn. negative is left, positive is right. Default value is zero.
        """

        if speed == None:
            speed = self.defaultSpeed

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
        """
        Stop driving instantly.
        """

        self.lMotor.stop()
        self.rMotor.stop()

    def straight(self, distance: float, speed: int) -> None:
        """
        Drives straight for a period of time.

        :param float distance:
        The amount of time that the robot drives for.

        :param int speed:
        The speed at which to drive at.
        """

        self.stop()

        self.straight(speed)

        timeToStop = process_time + distance
        while process_time < timeToStop:
            pass

        self.stop()
