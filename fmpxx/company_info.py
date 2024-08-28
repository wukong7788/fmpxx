import requests
import pandas as pd
import numpy as np
from typing import Dict, Any, List
from fmpxx.client import FMPClient


class CompanyInfo(FMPClient):
    def __init__(self, api_key: str, timeout: int = 10):
        super().__init__(api_key, timeout)

    def get_analyst_estimates(self, symbol: str) -> pd.DataFrame:
        """获取分析师估计数据"""
        endpoint = f"{self.url}/v3/analyst-estimates/{symbol}"
        response = self._handle_response(endpoint, {})
        return self.trans_to_df(response)

    def sp500_constituent(self) -> List[str]:
        """获取当前S&P 500成分股列表"""
        endpoint = f"{self.url}/v3/sp500_constituent"
        resp = self._handle_response(endpoint, {})
        return [i["symbol"] for i in resp]

    def sp500_his_list(self) -> List[str]:
        """获取历史和当前的S&P 500成分股完整列表"""
        endpoint = f"{self.url}/v3/historical/sp500_constituent"
        resp = self._handle_response(endpoint, {})
        df = pd.DataFrame.from_records(resp)
        
        # 处理日期和股票代码
        df["date"] = pd.to_datetime(df["date"])
        df["addedTicker"] = df.apply(lambda x: x["symbol"] if x["addedSecurity"] else np.nan, axis=1)
        df["removedTicker"] = df["removedTicker"].apply(lambda x: np.nan if len(x) == 0 else x)
        
        # 获取添加和移除的股票列表
        added = df["addedTicker"].dropna().tolist()
        removed = df["removedTicker"].dropna().tolist()
        
        # 合并当前和历史成分股
        full_list = self.sp500_constituent()
        full_list = sorted(list(set(full_list + added + removed)))
        
        # 数据清理
        full_list = [x for x in full_list if x != "NWSA" and ".A" not in x]
        
        return full_list
    
    
    def get_tickers(self, endpoint="v3/stock/list", **query_params):
        """
        获取股票列表
        
        返回约7500只股票，仅包含NASDAQ和NYSE交易所的普通股
        
        参数:
        - endpoint: API端点
        - query_params: 其他查询参数
        
        返回:
        - pd.DataFrame: 包含股票信息的数据框
        """
        full_endpoint = f"{self.url}/{endpoint}"
        response = self._handle_response(full_endpoint, query_params)
        
        df = self.trans_to_df(response)
        
        # 筛选普通股和主要交易所
        df = df[df["type"] == "stock"]
        df = df[df["exchangeShortName"].isin(["NASDAQ", "NYSE"])]
        
        return df.reset_index(drop=True)

    def get_available_tickers(self, endpoint="v3/available-traded/list", **query_params):
        """
        获取可交易的证券列表
        
        返回约8300只证券，包括股票、ETF、ETN等，仅限NASDAQ和NYSE交易所
        
        参数:
        - endpoint: API端点
        - query_params: 其他查询参数
        
        返回:
        - pd.DataFrame: 包含可交易证券信息的数据框
        """
        full_endpoint = f"{self.url}/{endpoint}"
        response = self._handle_response(full_endpoint, query_params)
        
        df = self.trans_to_df(response)
        
        # 筛选主要交易所
        df = df[df["exchangeShortName"].isin(["NASDAQ", "NYSE"])]
        
        return df.reset_index(drop=True)