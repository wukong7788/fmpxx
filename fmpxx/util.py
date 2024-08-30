from fmpxx.quote import Quote
from fmpxx.financials import Financials
import pandas as pd
from dotenv import load_dotenv, find_dotenv
import os
import logging

# 设置 pandas 显示选项
pd.set_option('display.max_rows', None)  # 显示所有行
pd.set_option('display.max_columns', None)  # 显示所有列
pd.set_option('display.width', None)  # 自动调整显示宽度
pd.set_option('display.max_colwidth', None)  # 显示完整的列内容
pd.set_option('future.no_silent_downcasting', True)

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s\n%(message)s')
logger = logging.getLogger(__name__)

def log(message, enable_logging):
    if enable_logging:
        logger.info(message)

def get_fiscal_close_chg(api_key: str, symbol: str, period: int, enable_logging: bool = False):
    """
    分析发布财报后close的变动
    """
    quote = Quote(api_key)
    financials = Financials(api_key)
    his_df = quote.get_stock_history(symbol, period=period)[['date', 'close']]

    eps_df = financials.get_earnings_his(symbol, period)
    eps_df = eps_df.sort_values(by='date', ascending=True, ignore_index=True)
    merged_df = pd.merge(eps_df, his_df, on='date', how='outer', sort=True)
    log(merged_df, enable_logging)
    # 可能会有周五盘后发布财报的情况，比如clsk，使用前值填充
    merged_df['close'] = merged_df['close'].ffill()
    log(merged_df, enable_logging)
    # 删除掉预估数据：删除date日期大于今天的行
    merged_df['date'] = pd.to_datetime(merged_df['date'])
    merged_df = merged_df[merged_df['date'] <= pd.Timestamp.now()]
    log(merged_df, enable_logging)
    
    # 计算is_fiscal=True时的close变动比率，考虑盘后发布财报的情况
    merged_df['fiscal_chg'] = merged_df['close'].pct_change()
    
    log(merged_df, enable_logging)
    # 只保留 is_fiscal 为 True 且不为 NA 的行
    merged_df = merged_df[merged_df['is_fiscal'].notnull() & merged_df['is_fiscal']]

    log(merged_df, enable_logging)
    # 后续根据导出情况，可以简化列
    return merged_df





def merge_eps_his(api_key: str, symbol: str, period: int, enable_logging: bool = True) -> pd.DataFrame:
    """
    生成pe和his的时序数据。
    注意：如果发布财报后使用需要等开盘数据，要不然没有close，最新的epsttm会被删除
    :param api_key: API密钥
    :param symbol: 股票代码
    :param period: 获取历史数据的年数
    :param enable_logging: 是否启用日志记录，默认为True
    :return: 包含PE计算结果的DataFrame
    """
    quote = Quote(api_key)
    financials = Financials(api_key)
    
    eps_df = financials.get_earnings_his(symbol, period)
    eps_df = eps_df.sort_values(by='date', ascending=True, ignore_index=True)
    log(eps_df, enable_logging)
    # eps为空时，使用epsEstimated，通常只有未来一个季度有预测数据，也就是只会补充一个季度的值
    eps_df['forward'] = eps_df['eps'].isnull()
    eps_df['eps'] = eps_df['eps'].fillna(eps_df['epsEstimated'])
    eps_df['eps_ttm'] = eps_df['eps'].rolling(4).sum()

    his_df = quote.get_stock_history(symbol, period=period)

    merged_df = pd.merge(eps_df, his_df, on='date', how='outer', sort=True)
    log(merged_df, enable_logging)
    # 使用fpe来计算eps ttm
    merged_df['eps_ttm'] = merged_df['eps_ttm'].bfill().ffill()
    merged_df['forward'] = merged_df['forward'].bfill()
    merged_df = merged_df.round(2)
    #
    # 计算市盈率(PE)：如果eps_ttm大于0，则用收盘价除以eps_ttm；否则PE为0，避免负值的情况
    merged_df['pe'] = merged_df.apply(lambda row: row['close'] / row['eps_ttm'] if row['eps_ttm'] > 0 else 0, axis=1)
    # 删除掉了未来没有close的行，以及周五盘后发布财报，导致周六多一行的情况
    selected = merged_df[['date', 'eps_ttm', 'pe', 'close', 'eps', 'forward']].dropna(subset=['close'])
    return selected   # pd.set_option('future.no_silent_downcasting', True)  用于避免此处的降级警告
  





if __name__ == '__main__':
    load_dotenv(find_dotenv())
    api_key = os.getenv("FMP")

    symbol = 'NVDA'
    # merged_df = merge_eps_his(api_key, symbol, period=1, enable_logging=True)
    # log(merged_df, True)

    print(get_fiscal_close_chg(api_key, symbol, period=2))

