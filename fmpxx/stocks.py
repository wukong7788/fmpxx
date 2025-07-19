from .base import _BaseClient
import pandas as pd

class Stocks(_BaseClient):
    """Client for FMP Stock API endpoints."""

    def __init__(self, api_key: str, timeout: int = 10, output_format: str = 'json'):
        super().__init__(api_key, timeout, output_format)

    def historical_price_full(self, symbol: str, series_type: str = None, from_date: str = None, to_date: str = None):
        """
        Get full historical daily prices for a given symbol.

        Args:
            symbol (str): Stock ticker symbol (e.g., 'AAPL').
            series_type (str, optional): Type of series (e.g., 'line').
            from_date (str, optional): Start date in YYYY-MM-DD format.
            to_date (str, optional): End date in YYYY-MM-DD format.

        Returns:
            list or pandas.DataFrame: Historical price data.
        """
        endpoint = f"historical-price-full/{symbol}"
        params = {}
        if series_type: params['serietype'] = series_type
        if from_date: params['from'] = from_date
        if to_date: params['to'] = to_date

        data = self._make_request(endpoint, params)
        if data and 'historical' in data:
            return self._process_response(data['historical'])
        return self._process_response(data)

    def daily_prices(self, symbol: str, from_date: str = None, to_date: str = None):
        """
        Get historical daily prices for a given symbol (line series).

        Args:
            symbol (str): Stock ticker symbol (e.g., 'AAPL').
            from_date (str, optional): Start date in YYYY-MM-DD format.
            to_date (str, optional): End date in YYYY-MM-DD format.

        Returns:
            list or pandas.DataFrame: Daily price data.
        """
        return self.historical_price_full(symbol, series_type='line', from_date=from_date, to_date=to_date)

    def stock_list(self):
        """
        Get a list of all available stocks.

        Returns:
            list or pandas.DataFrame: List of stocks.
        """
        endpoint = "stock/list"
        data = self._make_request(endpoint)
        return self._process_response(data)

    def quote(self, symbol: str):
        """
        Get real-time quote for a given symbol.

        Args:
            symbol (str): Stock ticker symbol (e.g., 'AAPL').

        Returns:
            list or pandas.DataFrame: Quote data.
        """
        endpoint = f"quote/{symbol}"
        data = self._make_request(endpoint)
        return self._process_response(data)

    def search(self, query: str, exchange: str = None, limit: int = 10):
        """
        Search for companies by name or symbol.

        Args:
            query (str): Search query.
            exchange (str, optional): Filter by exchange.
            limit (int): Number of results to return. Defaults to 10.

        Returns:
            list or pandas.DataFrame: Search results.
        """
        endpoint = "search"
        params = {'query': query, 'limit': limit}
        if exchange: params['exchange'] = exchange
        data = self._make_request(endpoint, params)
        return self._process_response(data)
