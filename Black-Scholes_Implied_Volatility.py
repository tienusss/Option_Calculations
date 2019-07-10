# import packages
from scipy.stats import norm
import numpy as np
import scipy as sq

# Functions of the script
def Call_BS_Value(S, X, r, T, v):
    # Calculates the value of a call option (Just the Black-Scholes formula for call options)
    # S is the share price at time T
    # X is the strike price
    # r is the risk-free interest rate
    # T is the time to maturity in years (days/365)
    # v is the volatility
    d_1 = (np.log(S / X) + (r + v ** 2 * 0.5) * T) / (v * np.sqrt(T))
    d_2 = d_1 - v * np.sqrt(T)
    return S * norm.cdf(d_1) - X * np.exp(-r * T) * norm.cdf(d_2)


def Call_IV_Obj_Function(S, X, r, T, v, Call_Price):
    # Objective function which sets market and model prices equal to zero (Function needed for Call_IV)
    # The parameters are explained in the Call_BS_Value function
    return Call_Price - Call_BS_Value(S, X, r, T, v)


def Call_IV(S, X, r, T, Call_Price, a=-2, b=2, xtol=0.000001):
    # Calculates the implied volatility for a call option with Brent's method
    # The first four parameters are explained in the Call_BS_Value function
    # Call_Price is the price of the call option
    # Last three variables are needed for Brent's method
    _S, _X, _r, _t, _Call_Price = S, X, r, T, Call_Price

    def fcn(v):
        return Call_IV_Obj_Function(_S, _X, _r, _t, v, _Call_Price)

    try:
        result = sq.optimize.brentq(fcn, a=a, b=b, xtol=xtol)
        return np.nan if result <= xtol else result
    except ValueError:
        return np.nan


def Put_BS_Value(S, X, r, T, v):
    # Calculates the value of a put option(Just the Black-Scholes formula for put options)
    # The parameters are explained in the Call_BS_Value function
    d_1 = (np.log(S / X) + (r + v ** 2 * 0.5) * T) / (v * np.sqrt(T))
    d_2 = d_1 - v * np.sqrt(T)
    return X * np.exp(-r * T) * norm.cdf(-d_2) - S * norm.cdf(-d_1)


def Put_IV_Obj_Function(S, X, r, T, v, Put_Price):
    # Objective function which sets market and model prices equal to zero (Function needed for Put_IV)
    # The parameters are explained in the Call_BS_Value function
    return Put_Price - Put_BS_Value(S, X, r, T, v)


def Put_IV(S, X, r, T, Put_Price, a=-2, b=2, xtol=0.000001):
    # Calculates the implied volatility for a put option with Brent's method
    # The first four parameters are explained in the Call_BS_Value function
    # Put_Price is the price of the call option
    # Last three variables are needed for Brent's method
    _S, _X, _r, _t, _Put_Price = S, X, r, T, Put_Price

    def fcn(v):
        return Put_IV_Obj_Function(_S, _X, _r, _t, v, _Put_Price)

    try:
        result = sq.optimize.brentq(fcn, a=a, b=b, xtol=xtol)
        return np.nan if result <= xtol else result
    except ValueError:
        return np.nan


def Calculate_IV_Call_Put(S, X, r, T, Option_Price, Put_or_Call):
    # This is a general function witch summarizes Call_IV and Put_IV (delivers the same results)
    # Can be used for a Lambda function within Pandas
    # The first four parameters are explained in the Call_BS_Value function
    # Put_or_Call:
    # 'C' returns the implied volatility of a call
    # 'P' returns the implied volatility of a put
    # Option_Price is the price of the option.

    if Put_or_Call == 'C':
        return Call_IV(S, X, r, T, Option_Price)
    if Put_or_Call == 'P':
        return Put_IV(S, X, r, T, Option_Price)
    else:
        return 'Neither call or put'

#Body of the script
Call_Price=Call_IV(100,80,0.01,1,23)
Call_Summarize=Calculate_IV_Call_Put(100,80,0.01,1,23,'C')
Put_Price=Put_IV(100,80,0.01,1,2)
Put_Summarize=Calculate_IV_Call_Put(100,80,0.01,1,2,'P')

#The output variables
print('The implied volatility of the European call option is '+str(Call_Price))
print('The implied volatility of the European call option is '+str(Call_Summarize))
print('The implied volatility of the European put option is '+str(Put_Price))
print('The implied volatility of the European put option is '+str(Put_Summarize))