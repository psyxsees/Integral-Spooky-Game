import random
from sympy import *

x = Symbol('x')

class IntegralSolver:
    def __init__(self):
        print("Integral Solver Initialized")

    def IntegralTerminal(self):
        ranInt = random.randint(0, 9)
        # ranInt = 5 #selectively for testing
        return {
            "equation": self.GetIntegral(ranInt),
            "int": self.Encrypt(),
            "der": self.Encrypt(),
            "rate": self.Encrypt(),
            "derivative": self.SolveDerivative(self.SolveIntegral(self.GetIntegral(ranInt))),
        }
        # integrated, derivative, and rate should be put into the encrypted fields when solved. Player shouldn't be able to see or access them until then.

    def Encrypt(self):
        symbols = "abcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*~/|\\_.- "
        length = random.randint(10, 30)
        return "".join(random.choice(symbols) for _ in range(length))

    def GetIntegral(self, ranInt):
        options = [
            "x*exp(x)",
            "log(x)",
            "x**2 * cos(x)",
            "exp(x) * sin(x)",
            "x * log(x)",
            "1/sqrt(x**2 - 9)",
            "x**2/sqrt(25 - x**2)",
            "1/((x**2+4)*sqrt(x**2))",
            "sqrt(x**2 + 16)",
            "1/((9 - x**2)**(Rational(3,2)))"
        ]
        return options[ranInt]

    def SolveIntegral(self, eq):
        #sympify(eq)
        return str(simplify(integrate(eq, x)))

    def SolveDerivative(self, eq):
        #sympify(eq)
        return simplify(diff(eq, x))

    def RateOfChange(self, eq, t):
        #sympify(eq)
        return simplify(eq.subs(x, t))

    def MakeReadable(self, expr):
        return str(expr).replace("**", "^").replace("exp", "e^")
