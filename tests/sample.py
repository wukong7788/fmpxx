import pandas as pd
from fmpxx import FMPClient
from fmpxx import Quote
from dotenv import load_dotenv, find_dotenv
import os
from fmpxx import Financials
from fmpxx import Info
pd.set_option('display.float_format', '{:.2f}'.format)
# pd.options.display.float_format = '{:.0f}'.format


load_dotenv(find_dotenv())
API_Key = os.getenv("FMP")
info = Info(API_Key)
symbols = ['AAPL','NVDA']
print(info.get_stock_news(symbols=symbols, period=3))

# client = FMPClient(api_key=API_Key)
#
# print(client.get_real_his_fmp("AAPL", period=1))
# print(fmp.get_8k_update(hasFinancial='true', limit=20))
# print(fmp.get_his_fmp('AAPL', period=1))
# print(fmp.get_quote_short('AAPL'))
# print(fmp.get_quote('AAPL'))
# print(fmp.get_real_his_fmp('AAPL', period=2))
# print(fmp.get_tickers())
# print(fmp.get_available_tickers())
# print(fmp.get_sec_update(3)['ticker'].tolist())


# get estimated eps/revenue
# company_info_client = CompanyInfo(API_Key)
# aapl_analyst_estimates = company_info_client.get_analyst_estimates("AAPL")
# print(aapl_analyst_estimates)

# get quote
# quote_client = Quote(API_Key)
# print(quote_client.get_simple_quote('AAPL'))
# print(quote_client.get_his_fmp('AAPL'))
# client = Financials(API_Key)
# # print(client.get_financials('ABT',statement='income'))
# # print(client.get_income_statement('ABT'))
# # print(client.get_eps('ABT'))
# print(client.get_earnings_his('TSM'))
# for symbol in ['NVDA', 'TSLA', 'MSFT', 'AAPL', 'AMZN', 'GOOGL', 'META']:

