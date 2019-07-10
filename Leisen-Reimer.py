# Import packages
import numpy as np


# Defined functions
def LeisenReimerBinomial(OutputFlag, AmeEurFlag, CallPutFlag, S, X, T, r, b, v, n):
    # This functions calculates the implied volatility of American and European options
    # This code is based on "The complete guide to Option Pricing Formulas" by Espen Gaarder Haug (2007)
    # Translated from a VBA code
    # OutputFlag:
    # "P" Returns the options price
    # "d" Returns the options delta
    # "a" Returns an array containing the option value, delta and gamma
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
    # b is the cost of carry rate
    # v is the volatility
    # n determines the stepsize

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
    d1 = (np.log(S / X) + (b + v ** 2 / 2) * T) / (v * np.sqrt(T))
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
    u = np.exp(b * dt) * hd1 / hd2
    d = (np.exp(b * dt) - p * u) / (1 - p)
    df = np.exp(-r * dt)

    # Determine if you want to exercise the option or not
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
        if j == 2:
            gamma = ((max_pay_off_list[2] - max_pay_off_list[1]) / (S * u ** 2 - S * u * d) - (
                    max_pay_off_list[1] - max_pay_off_list[0]) / (S * u * d - S * d ** 2)) / (
                            0.5 * (S * u ** 2 - S * d ** 2))
        if j == 1:
            delta = ((max_pay_off_list[1] - max_pay_off_list[0])) / (S * u - S * d)
    price = max_pay_off_list[0]

    # Put all the variables in the list
    variable_list = [delta, gamma, price]

    # Return values
    if OutputFlag == 'P':
        return price
    elif OutputFlag == 'd':
        return delta
    elif OutputFlag == 'g':
        return gamma
    elif OutputFlag == 'a':
        return variable_list
    else:
        return 'Indicate if you want to return P, d, g or a'


def round_up_to_odd(n):
    # This function returns a number rounded up to the nearest odd integer
    # For example when n = 100, the function returns 101
    return np.ceil(n) // 2 * 2 + 1

#Body of the script
Eur_call_result = LeisenReimerBinomial('P', 'e', 'C', 90, 100, 1, 0.01, 0.01, 0.2, 300)
American_call_result = LeisenReimerBinomial('P', 'a', 'C', 90, 100, 1, 0.01, 0.01, 0.2, 300)
Eur_put_result = LeisenReimerBinomial('P', 'e', 'P', 90, 100, 1, 0.01, 0.01, 0.2, 300)
American_put_result = LeisenReimerBinomial('P', 'a', 'P', 90, 100, 1, 0.01, 0.01, 0.2, 300)

#Print the output of the results
print('The price of the European call option is equal to ' +str(Eur_call_result))
print('The price of the American call option is equal to ' +str(American_call_result))
print('The price of the European put option is equal to ' +str(Eur_put_result))
print('The price of the American put option is equal to ' +str(American_put_result))
