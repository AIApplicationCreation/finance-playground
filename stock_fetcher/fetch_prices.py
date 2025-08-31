import argparse
import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

#parsing (getting info from user)
parser = argparse.ArgumentParser(description="Fetch stock prices")

parser.add_argument("--ticker", required = True, help = "Stock ticker symbol (e.g. AAPL, MSFT)")
parser.add_argument("--years", type = str, default = "5y", help = "Number of years of history to fetch (e.g. 1d, 5d, 1mo, 6mo, 1y, 5y, max)")
parser.add_argument("--short-dates", action = "store_true", help = "Format dates as 'Aug 25' instead of '2025-08-25'")

args = parser.parse_args()

#yfinance stuff
ticker = yf.Ticker(args.ticker)
history = ticker.history(period = f"{args.years}", interval = "1d")

#print to terminal
print(f"Ticker: {args.ticker}")
print(f"Years: {args.years}")
print(history.head())

#plot the closing prices
plt.figure(figsize = (10, 5))
plt.plot(history.index, history["Close"], label = "Close Price", color = "blue")

#x-axis label formatting
if args.short_dates:
    plt.xticks(history.index, history.index.strftime("%b %d"))
else:
    plt.xticks(history.index, history.index.date)

#title and labels
plt.title(f"{args.ticker} Stock Price ({args.years})", fontsize = 14)
plt.xlabel("Date")
plt.ylabel("Price (USD)")

#grid and legend
plt.grid(True, linestyle = "--", alpha = 0.6)
plt.legend()

#show the plot
plt.show()