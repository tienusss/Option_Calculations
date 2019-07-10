# Option_Calculations
In this repositories you can find script for calculating the prices and implied volatilities of plain-vanilla options (American and European).

# Leisen-Reimer.py
With the Leisen-Reimer.py script you are able to calculate the price for European- and American Plain-vanilla options (for options with non-dividend paying underlyings). There is also a functionality to return the delta, gamma and a list of the price, delta and gamma. This code is transalted from a VBA code in the book "The Complete Guide to Option Pricing Formulas" by Espen Gaarder Haug.

The script requires numpy.

# Black-Scholes_Implied_Volatility.py
With the Black-Scholes_Implied_Volatility.py script you are able to calculate the implied volatility of plain vanilla European options. The script is based on Black-Scholes and Brent's method is used to determine the implied volatility. You can use the Call_IV or Put_IV function for directly calculating the implied volatility of a call or put. Or you can use the Calculate_IV_Call_Put function for which have to indicate if the option is a call or put. Both methods deliver the same results.

The script requires scipy and numpy.

# Leisen-Reimer_IV.py
With the Leisen-Reimer_IV.py script you are able to calculate the implied volatiliy of plain vanilla European and American options. The script is based on the Leisen-Reimer method and Brent's method is used to determine the implied volatility.

The script requires scipy and numpy.

# Future updates
In the near future I will upload a Implied Volatility calculator for option with dividend paying underlyings (continous and discrete). Furthermore also a script to calculate the value of barrier options with the Black-Scholes formulas.
