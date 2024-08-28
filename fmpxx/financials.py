import pandas as pd
from fmpxx.client import FMPClient


class Financials(FMPClient):
    def __init__(self, api_key: str, timeout: int = 10):
        super().__init__(api_key, timeout)

    def get_income_statement(self, symbol: str) -> pd.DataFrame:
        """
        获取指定股票的季度收益报表。

        :param symbol: 股票代码
        :return: 包含收益报表数据的DataFrame
        """
        endpoint = f"{self.url}/v3/income-statement/{symbol}"
        params = {"period": "quarter", "limit": 20}
        response = self._handle_response(endpoint, params)
        return self.trans_to_df(response)

    def get_earnings_his(self, symbol: str, period: int = 3) -> pd.DataFrame:
        """
        获取指定股票的历史盈利日历。

        :param symbol: 股票代码
        :param period: 获取的年数，默认为3年
        :return: 包含历史盈利数据的DataFrame
        """
        endpoint = f"{self.url}/v3/historical/earning_calendar/{symbol}"
        params = {"limit": period * 4 + 4}  # 一般会有4个以内的空数据
        response = self._handle_response(endpoint, params)
        df = self.trans_to_df(response)
        
        # 添加date_adj列
        df['date_adj'] = pd.to_datetime(df['date'])
        df.loc[df['time'] == 'amc', 'date_adj'] += pd.Timedelta(days=1)
        
        # 删除原来的date列，并将date_adj重命名为date
        df = df.drop(columns=['date'])
        df = df.rename(columns={'date_adj': 'date'})
        
        # 将date列转换回object类型
        df['date'] = df['date'].dt.strftime('%Y-%m-%d')
        
        return df




