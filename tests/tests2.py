import sys
import os
import dotenv
import pandas as pd

# Set pandas display options for better output in console
# 不换行显示配置
pd.set_option('display.width', 1000)          # 宽度足够大
pd.set_option('display.max_columns', None)     # 显示所有列
pd.set_option('display.max_colwidth', 30)      # 限制单列宽度
pd.set_option('display.expand_frame_repr', False)  # 禁用折叠
pd.set_option('display.max_rows', None) 

# 获取项目根目录的绝对路径
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# 将项目根目录添加到 Python 模块搜索路径
sys.path.append(project_root)

# 然后再导入你的模块
from fmpxx import FMPClient
from fmpxx.exceptions import FMPAPIError, InvalidAPIKeyError, SymbolNotFoundError, RateLimitExceededError, FMPConnectionError

dotenv.load_dotenv()

API_Key = os.getenv("FMP_KEY")
ticker = 'AAPL' # Changed to AAPL for consistency

if not API_Key:
    print("Error: FMP_KEY environment variable not set. Please set it in your .env file or environment.")
    sys.exit(1)

client = FMPClient(api_key=API_Key, output_format='pandas')

print("\n--- Testing Financials ---")

# Test income statement
# print(f"Fetching income statement for {ticker}...")
income_statement = client.financials.get_financials(statement='income',symbol=ticker, limit=4)
# print("Income Statement (first row):\n", income_statement)
client.financials.get_merged_financials(symbol=ticker,limit=4).to_csv(f'tests/{ticker}.csv')
# print(client.stocks.historical_price_full(symbol=ticker,period=1))
