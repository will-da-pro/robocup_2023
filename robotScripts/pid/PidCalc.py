class PID:
    def __init__(self, error, pMult, iMult, dMult, lastError, pastErrors):
        self.error = error
        self.pMult = pMult
        self.iMult = iMult
        self.dMult = dMult

        self.lastError = lastError
        self.pastErrors = pastErrors

    
    def calcTurnRate(self):
        self.pastErrors = self.error+self.lastError
	
        pFix = self.error*self.pMult
	
        integral = self.lastError+self.pastErrors
        iFix = integral*self.iMult
	
        derivative = self.error-self.lastError
        dFix = derivative*self.dMult
	
        turnRate = (pFix+iFix+dFix)/3
        turnRate = round(turnRate,0)
        print("PID = "+str(turnRate))

        self.lastError = self.error
        

PID(100,1,1,1).calcTurnRate() #test