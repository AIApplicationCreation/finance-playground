import argparse
import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import sys

def main():

    # Parsing (getting info from user).
    parser = argparse.ArgumentParser(description="Fetch stock prices")
    parser.add_argument("--ticker", nargs = "+", required = True, help = "One or more stock ticker symbol (e.g., AAPL, MSFT)")
    parser.add_argument("--period", type = str, default = "5y", help = "The period of history to fetch (e.g., 1d, 5d, 1mo, 6mo, 1y, 5y, max)")
    parser.add_argument("--short-dates", action = "store_true", help = "Format dates as 'Aug 25' instead of '2025-08-25'")

    # Stores all of the information above.
    args = parser.parse_args()

    # Sets up the plot window.
    fig = plt.figure(figsize = (16, 4 * len(args.ticker)))

    # Sets up the normalized plot.
    ax_norm = plt.subplot2grid((len(args.ticker), 2), (0, 0), rowspan = len(args.ticker))

    # Sets up all of the other stock plots.
    axes = []
    for i in range(len(args.ticker)):
        ax = plt.subplot2grid((len(args.ticker), 2), (i, 1))
        axes.append(ax)

    # Prints the period to the terminal.
    print(f"Period: {args.period}")

    # A true/false statement for later.
    first_plotted = False

    # Prints info to terminal, adds info to normalized plot, adds info to and formats other stock plots.
    for t in args.ticker:
        # Prints the ticker of the stock.
        print(f"\n=== {t} ===")

        # Prints the stock info to the terminal.
        ticker = yf.Ticker(t)
        history = ticker.history(period = f"{args.period}", interval = "1d")
        print(history.head())

        # If the stock that corresponds to the ticker has no history, it prints the following statement and continues on.
        if history.empty:
            print(f"Warning: no data returned for {t}. Skipping")
            continue
        else:
            # Since there was history for at least one stock, it has plotted at least one of the graphs.
            first_plotted = True

        # The formula that normalizes all of the data so it can be compared.
        normalized = history['Close'] / history['Close'].iloc[0] * 100

        # Adds all of the stock information to the normalized graph
        ax_norm.plot(history.index, normalized, label = t)

        # Adds all of the relevant stock information to each corresponding stock plot
        axes[args.ticker.index(t)].plot(history.index, history["Close"], label = t)

        # Formats all the corresponding stock plots
        axes[args.ticker.index(t)].set_title(f"{t} Stock Price ({args.period})")
        axes[args.ticker.index(t)].set_ylabel("Price (USD)")
        axes[args.ticker.index(t)].grid(True, linestyle="--", alpha=0.6)
        axes[args.ticker.index(t)].legend()
        

    # If there was no history for any of the stocks, the system exits.
    if not first_plotted:
        print("No data fetched for any ticker. Exiting.")
        sys.exit(1)

    # Formats the normalized graph
    ax_norm.set_title("Normalized Performance (Start = 100)")
    ax_norm.set_ylabel("Normalized Price")
    ax_norm.legend()
    ax_norm.grid(True, linestyle="--", alpha = 0.6)

    # Creates a date locator
    locator = mdates.AutoDateLocator()

    # If the user wants to use short dates, they can. Otherwise it continues with long dates.
    if args.short_dates:
        fmt = mdates.DateFormatter("%b %d")
    else:
        fmt = mdates.DateFormatter("%Y-%m-%d")

    # Locates dates and formats them nicely for normalized graph.
    ax_norm.xaxis.set_major_locator(locator)
    ax_norm.xaxis.set_major_formatter(fmt)

    # Locates dates and formats them nicely for each stock plot.
    for ax in axes:
        ax.xaxis.set_major_locator(locator)
        ax.xaxis.set_major_formatter(fmt)

    # Tilts the dates and makes them look nice.
    plt.tight_layout()
    plt.gcf().autofmt_xdate()

    # Adds the word "Date" at the bottom of the plot window.
    fig.text(0.5, 0.04, "Date", ha = "center", va = "bottom", fontsize = 12)

    # Shows the plot
    plt.show()

if __name__ == "__main__":
    main()