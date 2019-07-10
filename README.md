# Option_Calculations
Python scripts to calculate a couple of options (financial derivatives) and Implied Volatilities for American and European options

# Leisen-Reimer.py
With the Leisen-Reimer.py script you are able to calculate the price for European- and American Plain-vanilla options (for options with non-dividend paying underlyings). There is also a functionality to return the delta, gamma and a list of the price, delta and gamma. This code is transalted from a VBA code in the book "The Complete Guide to Option Pricing Formulas" by Espen Gaarder Haug.

The script requires numpy.

# Black-Scholes_Implied_Volatility.py
With the Black-Scholes_Implied_Volatility.py script you are able to calculate the implied volatility for plain vanilla European options. The script is based on Black-Scholes and Brent's method is used to determine the implied volatility. You can use the Call_IV or Put_IV function for directly calculating the implied volatility of a call or put. Or you can use the Calculate_IV_Call_Put function for which have to indicate if the option is a call or put. Both methods deliver the same results.

The script requires scipy and numpy.

# Future updates
In the near future I will upload a Implied Volatility calculator based on Leisen-Reimer (European and American). Furthermore also a script to calculate the value of barrier options with the Black-Scholes formulas.
