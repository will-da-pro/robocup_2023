import gpiozero
from time import process_time

class driveBase():
    def __init__(self, port1: int, port2: int, port3: int, port4: int, defaultSpeed=100) -> None:
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

        self.defaultSpeed = max(0, min(defaultSpeed, 100))

    def drive(self, speed: int = None, turnAngle: int = 0) -> None:
        """
        Makes the robot drive. What did you think this did?

        :param int speed:
          Controls the speed at which to drive at. choose a number between -1000 and 1000.

        :param int turnAngle:
          A number that controls the speed at which to turn. negative is left, positive is right. Default value is zero.
        """

        if speed == None:
            speed = self.defaultSpeed
            
        turnAngle = max(-100, min(turnAngle, 100))
        
        lSpeed = 0
        rSpeed = 0
        
        if turnAngle < 0:
            rSpeed = -turnAngle * speed / 100
            lSpeed = (100 + turnAngle) * speed / 100
        else:
            rSpeed = (100 - turnAngle) * speed / 100
            lSpeed = turnAngle * speed / 100
            
        self.lMotor.forward(lSpeed)
        self.rMotor.forward(rSpeed)
        
        
    def stop(self) -> None:
        """
        Stops driving immediately.
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

        self.lMotor.forward(speed)
        self.rMotor.forward(speed)

        timeToStop = process_time + distance
        while process_time < timeToStop:
            pass

        self.stop()
