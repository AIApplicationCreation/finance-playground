import argparse
import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import sys

def main():
    #parsing (getting info from user)
    parser = argparse.ArgumentParser(description="Fetch stock prices")

    parser.add_argument("--ticker", nargs = "+", required = True, help = "One or more stock ticker symbol (e.g., AAPL, MSFT)")
    parser.add_argument("--period", type = str, default = "5y", help = "The period of history to fetch (e.g., 1d, 5d, 1mo, 6mo, 1y, 5y, max)")
    parser.add_argument("--short-dates", action = "store_true", help = "Format dates as 'Aug 25' instead of '2025-08-25'")

    args = parser.parse_args()

    plt.figure(figsize = (10, 5))
    first_plotted = False

    print(f"Period: {args.period}")

    for t in args.ticker:
        print(f"\n=== {t} ===")
        ticker = yf.Ticker(t)
        history = ticker.history(period = f"{args.period}", interval = "1d")
        normalized = history['Close'] / history['Close'].iloc[0] * 100
        print(history.head())

        if history.empty:
            print(f"Warning: no data returned for {t}. Skipping")
            continue
        
        plt.plot(history.index, history["Close"], label = t)
        first_plotted = True

    if not first_plotted:
        print("No data fetched for any ticker. Exiting.")
        sys.exit(1)

    #plot the closing prices

    # plt.plot(history.index, history["Close"], label = "Close Price", color = "blue")

    #x-axis label formatting
    if args.short_dates:
        plt.xticks(history.index, history.index.strftime("%b %d"))
    else:
        plt.xticks(history.index, history.index.date)

    #title and labels
    plt.title(f"{args.ticker} Stock Price ({args.period})", fontsize = 14)
    plt.xlabel("Date")
    plt.ylabel("Price (USD)")
    plt.gcf().autofmt_xdate()

    #grid and legend
    plt.grid(True, linestyle = "--", alpha = 0.6)
    plt.legend()

    #show the plot
    plt.show()

if __name__ == "__main__":
    main()