import os
import dotenv
from fmpxx import FMPClient
from fmpxx.exceptions import FMPAPIError, InvalidAPIKeyError, SymbolNotFoundError, RateLimitExceededError, FMPConnectionError
import pandas as pd

# Load environment variables
dotenv.load_dotenv()
API_KEY = os.getenv("FMP_KEY")

if not API_KEY:
    print("Error: FMP_KEY environment variable not set. Please set it in your .env file or environment.")
    exit(1)

client = FMPClient(api_key=API_KEY, output_format='pandas')

def call_financials_get_financials(symbol: str, statement: str, limit: int = 10, period: str = 'quarter'):
    """
    Example of calling client.financials.get_financials
    """
    print(f"\n--- Calling financials.get_financials for {symbol}, statement={statement}, period={period}, limit={limit} ---")
    try:
        data = client.financials.get_financials(symbol=symbol, statement=statement, limit=limit, period=period)
        if not data.empty:
            print(data.head())
        else:
            print(f"No data found for {symbol}'s {statement} statement.")
    except FMPAPIError as e:
        print(f"Error calling financials.get_financials: {e}")

def call_stocks_historical_price_full(symbol: str, start: str = None, end: str = None, period: int = None):
    """
    Example of calling client.stocks.historical_price_full
    """
    print(f"\n--- Calling stocks.historical_price_full for {symbol}, start={start}, end={end}, period={period} ---")
    try:
        data = client.stocks.historical_price_full(symbol=symbol, start=start, end=end, period=period)
        if not data.empty:
            print(data.head())
        else:
            print(f"No historical price data found for {symbol}.")
    except FMPAPIError as e:
        print(f"Error calling stocks.historical_price_full: {e}")

def call_stocks_quote(symbol: str):
    """
    Example of calling client.stocks.quote
    """
    print(f"\n--- Calling stocks.quote for {symbol} ---")
    try:
        data = client.stocks.quote(symbol=symbol)
        if not data.empty:
            print(data.head())
        else:
            print(f"No quote data found for {symbol}.")
    except FMPAPIError as e:
        print(f"Error calling stocks.quote: {e}")

def call_stocks_search(query: str, exchange: str = None, limit: int = 10):
    """
    Example of calling client.stocks.search
    """
    print(f"\n--- Calling stocks.search for query='{query}', exchange={exchange}, limit={limit} ---")
    try:
        data = client.stocks.search(query=query, exchange=exchange, limit=limit)
        if not data.empty:
            print(data.head())
        else:
            print(f"No search results found for '{query}'.")
    except FMPAPIError as e:
        print(f"Error calling stocks.search: {e}")

def call_financials_get_merged_financials(symbol: str, limit: int = 40, period: str = 'quarter'):
    """
    Example of calling client.financials.get_merged_financials
    """
    print(f"\n--- Calling financials.get_merged_financials for {symbol}, limit={limit}, period={period} ---")
    try:
        data = client.financials.get_merged_financials(symbol=symbol, limit=limit, period=period)
        if data is not None and not data.empty:
            print(data.head())
        else:
            print(f"No merged financials found for {symbol}.")
    except FMPAPIError as e:
        print(f"Error calling financials.get_merged_financials: {e}")

def call_stocks_daily_prices(symbol: str, start: str = None, end: str = None, period: int = None):
    """
    Example of calling client.stocks.daily_prices
    """
    print(f"\n--- Calling stocks.daily_prices for {symbol}, start={start}, end={end}, period={period} ---")
    try:
        data = client.stocks.daily_prices(symbol=symbol, start=start, end=end, period=period)
        if not data.empty:
            print(data.head())
        else:
            print(f"No daily price data found for {symbol}.")
    except FMPAPIError as e:
        print(f"Error calling stocks.daily_prices: {e}")


if __name__ == "__main__":
    # Example calls based on PRD user stories
    call_financials_get_financials(symbol='AAPL', statement='income', limit=1, period='quarter')
    call_stocks_historical_price_full(symbol='GOOG', period=5)
    call_stocks_quote(symbol='MSFT')
    call_stocks_search(query='Tesla', exchange='NASDAQ')
    call_financials_get_merged_financials(symbol='AMZN')
    call_stocks_daily_prices(symbol='IBM', start='2023-01-01', end='2023-01-31')