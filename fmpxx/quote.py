import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
from fmpxx import FMPClient

pd.set_option("expand_frame_repr", False)  # 当列太多时不换行
pd.set_option("display.max_rows", 5000)  # 最多显示数据的行数

class Quote(FMPClient):
    def __init__(self, api_key: str, timeout: int = 10):
        super().__init__(api_key, timeout)

    def get_simple_quote(self, symbol: str) -> pd.DataFrame:
        """
        获取简单报价数据。
        
        :param symbol: 股票代码
        :return: 包含简单报价数据的 DataFrame
        """
        endpoint = f"{self.url}/v3/quote-short/{symbol}"
        response = self._handle_response(endpoint, {})
        return self.trans_to_df(response)

    def get_full_quote(self, symbol: str) -> pd.DataFrame:
        """
        获取完整报价数据。
        
        :param symbol: 股票代码
        :return: 包含完整报价数据的 DataFrame
        """
        endpoint = f"{self.url}/v3/quote/{symbol}"
        response = self._handle_response(endpoint, {})
        return self.trans_to_df(response)
    
    def get_his_daily(self, symbol: str, period: int) -> pd.DataFrame:
        """
        获取指定股票的历史数据，已经包含了开盘当天的数据

        :param symbol: 股票代码
        :param period: 获取的年数
        :return: 包含历史数据的DataFrame
        """
        endpoint = f"{self.url}/v3/historical-price-full/{symbol}"
        
        to_date = datetime.now().strftime("%Y-%m-%d")
        from_date = (datetime.now() - relativedelta(years=period)).strftime("%Y-%m-%d")
        
        params = {
            "from": from_date,
            "to": to_date
        }
        
        response = self._handle_response(endpoint, params)
        
        if "historical" not in response:
            print(f"未找到 {symbol} 的历史数据")
            return pd.DataFrame()
        
        df = pd.DataFrame(response["historical"])
        df = df.drop(columns=["unadjustedVolume", "change", "changePercent", "vwap", "label", "changeOverTime", "adjClose"], errors="ignore")
        # 只有在合成数据时才使用转换
        # df["date"] = pd.to_datetime(df["date"])
        # 清洗数据
        df["date"].dropna(inplace=True)
        df["date"].drop_duplicates(inplace=True)
        df.sort_values(by=["date"], ignore_index=True, inplace=True)
        df["pct"] = df["close"].pct_change()
        
        return df


