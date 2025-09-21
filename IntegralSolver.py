import random
from sympy import *

x = Symbol('x');
class IntegralSolver:
    def __init__(self):
        print("Integral Solver Initialized");

    def IntegralTerminal(self):
        integral = []
        randomInt = random.randint(0, 9)
        integral.append(self.GetIntegral(randomInt))
        # giving the command line something to get back
        integral.append(self.Encrypt())
        integral.append(self.Encrypt())
        integral.append(self.Encrypt())

        integral.insert(0, random.randint(0, 1000000)) # ID for the integral
        return integral

    def Encrypt(self):
        symbols = "abcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*~/|\_.- "
        randomSymbol = 0
        randomRange = random.randint(10, 30)
        encryptedStr = ""

        for i in range(randomRange):
            randomSymbol = random.randint(0, 52)
            encryptedStr += symbols[randomSymbol]
        return encryptedStr

    def GetIntegral(self, ranInt):
        if (ranInt == 0):
            return "x*exp(x)"
        elif (ranInt == 1):
            return "log(x)"
        elif (ranInt == 2):
            return "x**2 * cos(x)"
        elif (ranInt == 3):
            return "exp(x) * sin(x)"
        elif (ranInt == 4):
            return "x * log(x)"
        elif (ranInt == 5):
            return "1/sqrt(x**2 - 9)"
        elif (ranInt == 6):
            return "x**2/sqrt(25 - x**2)"
        elif (ranInt == 7):
            return "1/((x**2+4)*sqrt(x**2))"
        elif (ranInt == 8):
            return "sqrt(x**2 + 16)"
        elif (ranInt == 9):
            return "1/((9 - x**2)**(Rational(3,2)))"

    def SolveIntegral(self, integral):
        return simplify(integrate(integral, x))

    def SolveDerivative(self, eq):
        return simplify(diff(eq, x))

    def RateOfChange(self, eq, t):
        return eq.subs(x, t)

    def MakeReadable(self, integral):
        return str(integral).replace("**", "^").replace("exp", "e^")