# Simple_Technical_Stock_Analyzer
Python scripts for obtaining the return for several periods and plotting stock price variations

## stock_retriever.py
Obtains the 1-year, 6-month, 3-month, 1-month, and 1-week returns on a set of stocks along with its current price and volatility. Then, it creates a composite score based on the returns with custom weights for the return for each period, and returns the sorted table of stocks with the obtained indices as an Excel file.

## stock_plotter_int.py
Uses IEX Cloud dataset to create interactive plots (in HTML) of the weekly and monthly variations for a set of indices.
