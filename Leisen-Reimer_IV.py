# Import packages
import numpy as np
from scipy.optimize import fsolve
import scipy as sq


# Defined functions
def LeisenReimerBinomial(AmeEurFlag, CallPutFlag, S, X, T, r, c, v, n):
    # This functions calculates the implied volatility of American and European options
    # This code is based on "The complete guide to Option Pricing Formulas" by Espen Gaarder Haug (2007)
    # Translated from a VBA code
    # AmeEurFlag:
    # "a" Returns the American option value
    # "e" Returns the European option value
    # CallPutFlag:
    # "C" Returns the call value
    # "P" Returns the put value
    # S is the share price at time t
    # X is the strike price
    # T is the time to maturity in years (days/365)
    # r is the risk-free interest rate
    # c is the cost of carry rate
    # v is the volatility
    # n determines the step size

    # Start of the code
    # rounds n up tot the nearest odd integer (the function is displayed below the LeisenReimerBinomial function in line x)
    n = round_up_to_odd(n)

    # Creates a list with values from 0 up to n (which will be used to determine to exercise or not)
    n_list = np.arange(0, (n + 1), 1)

    # Checks if the input option is a put or a call, if not it returns an error
    if CallPutFlag == 'C':
        z = 1
    elif CallPutFlag == 'P':
        z = -1
    else:
        return 'Call or put not defined'

    # d1 and d2 formulas of the Black-Scholes formula for European options
    d1 = (np.log(S / X) + (c + v ** 2 / 2) * T) / (v * np.sqrt(T))
    d2 = d1 - v * np.sqrt(T)

    # The Preizer-Pratt inversion method 1
    hd1 = 0.5 + np.sign(d1) * (0.25 - 0.25 * np.exp(-(d1 / (n + 1 / 3 + 0.1 / (n + 1))) ** 2 * (n + 1 / 6))) ** 0.5

    # The Preizer-Prat inversion method 2
    hd2 = 0.5 + np.sign(d2) * (0.25 - 0.25 * np.exp(-(d2 / (n + 1 / 3 + 0.1 / (n + 1))) ** 2 * (n + 1 / 6))) ** 0.5

    # Calculates the stepsize in years
    dt = T / n

    # The probability of going up
    p = hd2

    # The up and down factors
    u = np.exp(c * dt) * hd1 / hd2
    d = (np.exp(c * dt) - p * u) / (1 - p)
    df = np.exp(-r * dt)

    # Creates the most right column of the three
    max_pay_off_list = []
    for i in n_list:
        i = i.astype('int')
        max_pay_off = np.maximum(0, z * (S * u ** i * d ** (n - i) - X))
        max_pay_off_list.append(max_pay_off)

    # The binominal tree
    for j in np.arange(n - 1, 0 - 1, -1):
        for i in np.arange(0, j + 1, 1):
            i = i.astype(int)  # Need to be converted to a integer
            if AmeEurFlag == 'e':
                max_pay_off_list[i] = (p * max_pay_off_list[i + 1] + (1 - p) * max_pay_off_list[i]) * df
            elif AmeEurFlag == 'a':
                max_pay_off_list[i] = np.maximum((z * (S * u ** i * d ** (j - i) - X)),
                                                 (p * max_pay_off_list[i + 1] + (1 - p) * max_pay_off_list[i]) * df)
    price = max_pay_off_list[0]

    return price


def round_up_to_odd(n):
    # This function returns a number rounded up to the nearest odd integer
    # For example when n = 100, the function returns 101
    return np.ceil(n) // 2 * 2 + 1


def IV_solver(AmeEurFlag, CallPutFlag, S, X, T, r, c, n, Option_Value):
    # This function is the implied volatility solver which makes use of Brent's methods
    # The paramaters are the same as described as in LeisenReimerBinomial function, except for Option_Value
    # Option_Value is the parameter of the option value (for which you want to calculate the Implied Volatility)
    def objection_function(IV):
        # This is the objection function
        result = Option_Value - LeisenReimerBinomial(AmeEurFlag, CallPutFlag, S, X, T, r, c, IV, n)
        return result

    IV_Result = sq.optimize.brentq(objection_function, a=0.1, b=2, xtol=0.000001)
    # a and b repesent the intervals ([a,b]) and xtol determines the precision
    return IV_Result


# Body of the script to show that the IV solver works

# This functions calculates the value of an American put option and prints the result
optionvalue = LeisenReimerBinomial('a', 'P', 100, 100, 1, 0.01, 0.01, 0.50, 400)
print('The value of an American put option, with IV of 50% is equal to '+str(optionvalue))
IV_value=IV_solver('a','P',100,100,1,0.01,0.01,400,optionvalue)
print('The implied volatility is '+str(IV_value))
