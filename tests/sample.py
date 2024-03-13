from fmpx.client import FMPClient
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())
API_Key = os.getenv("FMP_KEY")

client = FMPClient(api_key=API_Key)

print(client.get_real_his_fmp("AAPL", period=1))
# print(fmp.get_8k_update(hasFinancial='true', limit=20))
# print(fmp.get_his_fmp('AAPL', period=1))
# print(fmp.get_quote_short('AAPL'))
# print(fmp.get_quote('AAPL'))
# print(fmp.get_real_his_fmp('AAPL', period=2))
# print(fmp.get_tickers())
# print(fmp.get_available_tickers())
# print(fmp.get_sec_update(3)['ticker'].tolist())
