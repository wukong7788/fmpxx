import sys
import os

# 获取项目根目录的绝对路径
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# 将项目根目录添加到 Python 模块搜索路径
sys.path.append(project_root)

# 然后再导入你的模块
from fmpxx import FMPClient, Quote

from fmpxx.financials import Financials
import os
import dotenv

dotenv.load_dotenv()

API_Key = os.getenv("FMP_KEY")
ticker = 'aapl'
fin = Financials(API_Key)
# print(fin.get_income_statement(ticker))
print(fin.get_earnings_his(ticker))

# print(client.get_earnings_his('NVDA', period=1))

# quote = Quote(api_key=API_Key)
# print(quote.get_his_daily(symbol='aapl', period=1))
# print(quote.get_simple_quote('aapl'))
# print(quote.get_full_quote('aapl'))

