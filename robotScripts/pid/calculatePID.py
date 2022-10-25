import cv2
import numpy
import picamera

class PID:
    def __init__(self, multiplier, camera):
        self.multiplier = multiplier
        self.camera = camera
        self.errorSum = 0
        self.lastError = 0
        self.error = 0

    def calculateTurnRate(self) -> float:
        error = self.calculateError()
        integral = self.calculateIntegral()
        derivative = self.calculateDerivative()

        turnRate = (error + integral + derivative) / 3

        return turnRate

    def calculateError(self) -> float:
        #TODO add error code
        self.lastError = self.error
        self.error = 0
        
        return error

    def calculateIntegral(self) -> float:
        integral = self.errorSum * self.multiplier
        
        return integral

    def calculateDerivative(self) -> float:
        derivative = (self.error - self.lastError) * self.multiplier

        return derivative