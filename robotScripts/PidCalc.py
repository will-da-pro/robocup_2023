class PID:
    def __init__(self, error, pMult, iMult, dMult, lastError, pastErrors):
        self.error = error
        self.pMult = pMult
        self.iMult = iMult
        self.dMult = dMult

        self.lastError = lastError
        self.pastErrors = pastErrors

    
    def calcTurnRate(self):
        pFix = self.error*self.pMult
	
        integral = self.lastError+self.pastErrors
        iFix = integral*self.iMult
	
        derivative = self.error-self.lastError
        dFix = derivative*self.dMult
	
        turnRate = pFix+iFix+dFix
        turnRate = round(turnRate,0)
        return turnRate