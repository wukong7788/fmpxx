import pandas as pd

from fmpxx.client import FMPClient
from fmpxx.company_info import CompanyInfo
from fmpxx.quote import Quote
from dotenv import load_dotenv, find_dotenv
import os
from fmpxx.financials import Financials
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

load_dotenv(find_dotenv())
API_Key = os.getenv("FMP_KEY")

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
client = Financials(API_Key)
# # print(client.get_financials('ABT',statement='income'))
# # print(client.get_income_statement('ABT'))
# # print(client.get_eps('ABT'))
# print(client.get_earnings_his('TSM'))
# for symbol in ['NVDA', 'TSLA', 'MSFT', 'AAPL', 'AMZN', 'GOOGL', 'META']:
for symbol in ['META']:

    df = client.get_pe(symbol, pe='est')
    # 将'date'列设置为索引
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    print(df)
    # #
    # 创建图表和轴对象
    fig, ax1 = plt.subplots()
    # 绘制第一条曲线（'close'），使用ax1
    color = 'tab:red'
    ax1.set_xlabel('date')
    ax1.set_ylabel('close', color=color)
    ax1.plot(df.index, df['close'], color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    # 创建与ax1共享横轴的第二个轴对象
    ax2 = ax1.twinx()
    color = 'tab:blue'
    ax2.set_ylabel('PE', color=color)
    ax2.plot(df.index, df['pe'], color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    # 设置x轴的主要刻度格式器为日期格式器，这里我们每5天显示一次日期
    ax1.xaxis.set_major_locator(mdates.DayLocator(interval=90))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

    # 自动调整x轴上的日期标签，以防重叠
    fig.autofmt_xdate()
    plt.title(symbol)
    # 显示图表
    # plt.show()

    plt.savefig(f'{symbol}.png', dpi=150)