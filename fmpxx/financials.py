import logging
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from fmpxx.client import FMPClient
from retry import retry

# 配置日志
logger = logging.getLogger(__name__)

class Financials(FMPClient):
    """
    FMP财务数据客户端类，用于获取和处理财务数据。

    Attributes:
        api_key (str): API密钥
        timeout (int): 请求超时时间
    """
    def __init__(self, api_key: str, timeout: int = 10) -> None:
        """
        初始化Financials实例。

        Args:
            api_key (str): API密钥
            timeout (int): 请求超时时间，默认为10秒
        """
        super().__init__(api_key, timeout)


    @retry(tries=5, delay=5)
    def get_financials(
        self,
        symbol: str,
        statement: str,
        endpoint: str = "",
        **query_params: Dict[str, Any]
    ) -> pd.DataFrame:
        """
        获取指定类型的财务报表数据。

        Args:
            symbol (str): 股票代码
            statement (str): 报表类型，可选值：'income', 'balance', 'cash'
            endpoint (str): 自定义API端点
            **query_params: 其他查询参数

        Returns:
            pd.DataFrame: 包含财务报表数据的DataFrame

        Raises:
            ValueError: 如果statement参数无效
        """
        # 映射报表类型到API端点
        endpoint_map = {
            "income": "v3/income-statement",
            "balance": "v3/balance-sheet-statement", 
            "cash": "v3/cash-flow-statement"
        }

        if statement not in endpoint_map:
            raise ValueError(f"Invalid statement type: {statement}")

        endpoint = f"{self.url}/{endpoint_map[statement]}/{symbol}"
        res = self._handle_response(endpoint, query_params)
        
        if not res:
            logger.warning(f"获取{symbol}的{statement}报表数据失败")
            return pd.DataFrame()

        df = pd.DataFrame.from_records(res)
        return df.drop(columns=["link", "finalLink"], errors="ignore")

    def get_merged_financials(self, symbol: str) -> Optional[pd.DataFrame]:
        """
        合并现金流量表、损益表和资产负债表三张财务报表。

        Args:
            symbol (str): 股票代码

        Returns:
            Optional[pd.DataFrame]: 合并后的财务报表DataFrame，如果数据无效则返回None

        Note:
            - 使用inner join确保三张报表数据完整
            - 处理特殊股票的数据异常
            - 检查数据连续性和完整性
        """
        # 获取三张财务报表
        income = self.get_financials(symbol, statement="income", period="quarter", limit=40)
        balance = self.get_financials(symbol, statement="balance", period="quarter", limit=40)
        cash = self.get_financials(symbol, statement="cash", period="quarter", limit=40)

        # 检查数据完整性
        if income.empty or balance.empty or cash.empty:
            logger.warning(f"{symbol}的财务报表数据不完整")
            return None

        # 定义合并键
        on_list = [
            "cik", "fillingDate", "date", "symbol", 
            "period", "calendarYear", "reportedCurrency"
        ]

        # 合并财务报表
        merged_df = pd.merge(
            pd.merge(income, balance, how="inner", on=on_list),
            cash, how="inner", on=on_list
        )

        # 数据清洗和转换
        merged_df = (
            merged_df.rename(columns={
                "date": "period_date",
                "fillingDate": "date",
                "netIncome_x": "netIncome"
            })
            .sort_values(by=["date", "acceptedDate_x"], ignore_index=True)
            .drop_duplicates(subset=["date"], keep="first", ignore_index=True)
            .assign(period_date=lambda x: pd.to_datetime(x["period_date"]))
        )

        # 处理特殊股票
        special_symbols = [
            "ADT", "ALTR", "ARNC", "BEAM", "CEG", "CSC", "CTLT", "FTV", 
            "HLT", "HPE", "LDOS", "LW", "MMI", "MRNA", "OTIS", "PLL", 
            "S", "TWTR", "VNT"
        ]
        
        if symbol in special_symbols:
            merged_df = merged_df.drop([0]).reset_index(drop=True)

        # 检查数据连续性
        merged_df["verify"] = merged_df["period_date"].diff()
        if symbol == "CSC":
            return None

        # 验证数据周期
        for days in merged_df["verify"].tolist()[1:]:
            if days.days > 150:  # 正常间隔约91天
                logger.warning(f"{symbol}财报异常，数据周期不全")
                return None

        # 最终清理
        return (
            merged_df.drop(columns=["verify"])
            .fillna(value=0)
        )




    def get_8k_update(
        self, 
        endpoint: str = "v4/rss_feed_8k", 
        **query_params: Dict[str, Any]
    ) -> pd.DataFrame:
        """
        获取8-K报告更新。

        Args:
            endpoint (str): API端点，默认为"v4/rss_feed_8k"
            **query_params: 其他查询参数

        Returns:
            pd.DataFrame: 包含8-K报告更新的DataFrame
        """
        endpoint = f"{self.url}/{endpoint}"
        res = self._handle_response(endpoint, query_params)
        if not res:
            logger.warning("获取8-K报告更新失败")
            return pd.DataFrame()
        return self.trans_to_df(res)

    def get_sec_update(self, days: int) -> pd.DataFrame:
        """
        获取SEC更新。

        Args:
            days (int): 查询的天数范围

        Returns:
            pd.DataFrame: 包含SEC更新的DataFrame
        """
        end = datetime.today()
        start = end - timedelta(days=days)
        
        endpoint = (
            f"{self.url}/v4/rss_feed?"
            f"type=10&from={start.strftime('%Y-%m-%d')}&"
            f"to={end.strftime('%Y-%m-%d')}&isDone=true"
        )
        
        res = self._handle_response(endpoint, {})
        if not res:
            logger.warning("获取SEC更新失败")
            return pd.DataFrame()
        return self.trans_to_df(res)

    def get_income_statement(self, symbol: str) -> pd.DataFrame:
        """
        获取指定股票的季度收益报表。

        Args:
            symbol (str): 股票代码

        Returns:
            pd.DataFrame: 包含收益报表数据的DataFrame
        """
        endpoint = f"{self.url}/v3/income-statement/{symbol}"
        params = {"period": "quarter", "limit": 20}
        response = self._handle_response(endpoint, params)
        if not response:
            logger.warning(f"获取{symbol}的收益报表失败")
            return pd.DataFrame()
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
        # 此处因为已经调整了财报日对应的close，所以不用再根据盘前盘后计算close change
        df.loc[df['time'] == 'amc', 'date_adj'] += pd.Timedelta(days=1)
        
        # 删除原来的date列，并将date_adj重命名为date
        df = df.drop(columns=['date'])
        df = df.rename(columns={'date_adj': 'date'})
        
        # 添加is_fiscal列，用于判断是否是财报发布日
        df['is_fiscal'] = True
        # 将date列转换回object类型
        df['date'] = df['date'].dt.strftime('%Y-%m-%d')
        
        return df

