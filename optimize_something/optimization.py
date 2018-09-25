"""MC1-P2: Optimize a portfolio.  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
Copyright 2018, Georgia Institute of Technology (Georgia Tech)  		   	  			    		  		  		    	 		 		   		 		  
Atlanta, Georgia 30332  		   	  			    		  		  		    	 		 		   		 		  
All Rights Reserved  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
Template code for CS 4646/7646  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
Georgia Tech asserts copyright ownership of this template and all derivative  		   	  			    		  		  		    	 		 		   		 		  
works, including solutions to the projects assigned in this course. Students  		   	  			    		  		  		    	 		 		   		 		  
and other users of this template code are advised not to share it with others  		   	  			    		  		  		    	 		 		   		 		  
or to make it available on publicly viewable websites including repositories  		   	  			    		  		  		    	 		 		   		 		  
such as github and gitlab.  This copyright statement should not be removed  		   	  			    		  		  		    	 		 		   		 		  
or edited.  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
We do grant permission to share solutions privately with non-students such  		   	  			    		  		  		    	 		 		   		 		  
as potential employers. However, sharing with other current or future  		   	  			    		  		  		    	 		 		   		 		  
students of CS 7646 is prohibited and subject to being investigated as a  		   	  			    		  		  		    	 		 		   		 		  
GT honor code violation.  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
-----do not edit anything above this line---  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
Student Name: Tucker Balch (replace with your name)  		   	  			    		  		  		    	 		 		   		 		  
GT User ID: tb34 (replace with your User ID)  		   	  			    		  		  		    	 		 		   		 		  
GT ID: 900897987 (replace with your GT ID)  		   	  			    		  		  		    	 		 		   		 		  
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
from util import get_data, plot_data
import scipy.optimize as spo


def daily_returns_func(allocations, data):
    allocated = np.zeros(data.shape[0])
    for i, alloc in enumerate(allocations):
        allocated += data.iloc[:, i] * alloc

    daily_returns = allocated
    daily_returns[1:] = (allocated[1:] / allocated[:-1].values) - 1.0
    daily_returns.ix[0] = 0.0
    return daily_returns


def error_fuc(allocations, data, risk_free_rate=0.0):
    daily_returns = daily_returns_func(allocations, data)
    return -np.mean(daily_returns - risk_free_rate) / np.std(daily_returns)


# This is the function that will be tested by the autograder  		   	  			    		  		  		    	 		 		   		 		  
# The student must update this code to properly implement the functionality  		   	  			    		  		  		    	 		 		   		 		  
def optimize_portfolio(sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 1, 1), \
                       syms=['GOOG', 'AAPL', 'GLD', 'XOM'], gen_plot=False):
    # Read in adjusted closing prices for given symbols, date range  		   	  			    		  		  		    	 		 		   		 		  
    dates = pd.date_range(sd, ed)
    prices_all = get_data(syms, dates)  # automatically adds SPY  		   	  			    		  		  		    	 		 		   		 		  
    prices = prices_all[syms]  # only portfolio symbols  		   	  			    		  		  		    	 		 		   		 		  
    prices_SPY = prices_all['SPY']  # only SPY, for comparison later

    prices_normed = prices / prices.ix[0, :]
    initial_guess = np.full(len(syms), 1.0 / len(syms))
    result = spo.minimize(error_fuc, initial_guess,
                          args=(prices_normed),
                          method='SLSQP',
                          bounds=[(0, 1) for _ in syms],
                          tol=0.000001,
                          options={'display': True},
                          constraints={'type': 'eq', 'fun': lambda x: np.sum(x) - 1})

    # find the allocations for the optimal portfolio  		   	  			    		  		  		    	 		 		   		 		  
    # note that the values here ARE NOT meant to be correct for a test case
    cr, adr, sddr, sr = [0.25, 0.001, 0.0005, 0.2]  # add code here to compute stats

    allocations = result.x
    allocated = np.zeros(prices.shape[0])
    for i, alloc in enumerate(allocations):
        allocated += prices.iloc[:, i] * alloc

    cr = (allocated / allocated[0]) - 1.0
    adr = daily_returns_func(allocations, prices)
    sddr = np.std(adr)
    sr = -error_fuc(allocations, prices)

    # Get daily portfolio value  		   	  			    		  		  		    	 		 		   		 		  
    port_val = prices_SPY  # add code here to compute daily portfolio values

    # Compare daily portfolio value with SPY using a normalized plot  		   	  			    		  		  		    	 		 		   		 		  
    if gen_plot:
        # add code to plot here  		   	  			    		  		  		    	 		 		   		 		  
        df_temp = pd.concat([port_val, prices_SPY], keys=['Portfolio', 'SPY'], axis=1)
        pass

    return allocations, cr, adr, sddr, sr


def test_code():
    # This function WILL NOT be called by the auto grader  		   	  			    		  		  		    	 		 		   		 		  
    # Do not assume that any variables defined here are available to your function/code  		   	  			    		  		  		    	 		 		   		 		  
    # It is only here to help you set up and test your code  		   	  			    		  		  		    	 		 		   		 		  

    # Define input parameters  		   	  			    		  		  		    	 		 		   		 		  
    # Note that ALL of these values will be set to different values by  		   	  			    		  		  		    	 		 		   		 		  
    # the autograder!  		   	  			    		  		  		    	 		 		   		 		  

    start_date = dt.datetime(2009, 1, 1)
    end_date = dt.datetime(2010, 1, 1)
    symbols = ['GOOG', 'AAPL', 'GLD', 'XOM', 'IBM']

    # Assess the portfolio  		   	  			    		  		  		    	 		 		   		 		  
    allocations, cr, adr, sddr, sr = optimize_portfolio(sd=start_date, ed=end_date, \
                                                        syms=symbols, \
                                                        gen_plot=False)

    # Print statistics  		   	  			    		  		  		    	 		 		   		 		  
    print "Start Date:", start_date
    print "End Date:", end_date
    print "Symbols:", symbols
    print "Allocations:", allocations
    print "Sharpe Ratio:", sr
    print "Volatility (stdev of daily returns):", sddr
    print "Average Daily Return:", adr
    print "Cumulative Return:", cr


if __name__ == "__main__":
    # This code WILL NOT be called by the auto grader  		   	  			    		  		  		    	 		 		   		 		  
    # Do not assume that it will be called  		   	  			    		  		  		    	 		 		   		 		  
    test_code()
