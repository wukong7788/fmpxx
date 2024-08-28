from fmpxx.quote import Quote
from fmpxx.financials import Financials
import pandas as pd
from dotenv import load_dotenv, find_dotenv
import os
# 设置 pandas 显示选项
pd.set_option('display.max_rows', None)  # 显示所有行
pd.set_option('display.max_columns', None)  # 显示所有列
pd.set_option('display.width', None)  # 自动调整显示宽度
pd.set_option('display.max_colwidth', None)  # 显示完整的列内容


def merge_eps_his(api_key: str, symbol: str, period: int) -> pd.DataFrame:
    """
    生成pe和his的时序数据。

    :param api_key: API密钥
    :param symbol: 股票代码
    :param period: 获取历史数据的年数
    :param pe: 'now' 表示使用当前数据，'est' 表示使用估计数据
    :return: 包含PE计算结果的DataFrame
    """
    quote = Quote(api_key)
    financials = Financials(api_key)
    
    eps_df = financials.get_earnings_his(symbol, period)
    eps_df = eps_df.sort_values(by='date', ascending=True, ignore_index=True)
    print(eps_df)
    # eps为空时，使用epsEstimated，通常只有未来一个季度有预测数据，也就是只会补充一个季度的值
    eps_df['forward'] = eps_df['eps'].isnull()
    eps_df['eps'] = eps_df['eps'].fillna(eps_df['epsEstimated'])
    eps_df['eps_ttm'] = eps_df['eps'].rolling(4).sum()

    his_df = quote.get_stock_history(symbol, period=period)
    # fixme 如果碰到earnings是周五盘后发布的，会出现周六数据，需要调整
    merged_df = pd.merge(eps_df, his_df, on='date', how='outer', sort=True)
    # 使用fpe来计算eps ttm
    merged_df['eps_ttm'] = merged_df['eps_ttm'].fillna(method='bfill').fillna(method='ffill')
    merged_df['forward'] = merged_df['forward'].fillna(method='bfill')
    merged_df = merged_df.round(2)
    #
    # 计算市盈率(PE)：如果eps_ttm大于0，则用收盘价除以eps_ttm；否则PE为0，避免负值的情况
    merged_df['pe'] = merged_df.apply(lambda row: row['close'] / row['eps_ttm'] if row['eps_ttm'] > 0 else 0, axis=1)

    selected = merged_df[['date', 'eps_ttm', 'pe', 'close', 'eps', 'forward']].dropna(subset=['close'])
    return selected


if __name__ == '__main__':
    load_dotenv(find_dotenv())
    api_key = os.getenv("FMP")

    symbol = 'AAPL'
    pe = 'fpe'
    merged_df = merge_eps_his(api_key, symbol, period=1, pe=pe)
    print(merged_df)
