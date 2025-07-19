from .base import _BaseClient
import pandas as pd
import logging
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class Financials(_BaseClient):
    """Client for FMP Company Fundamentals API endpoints."""

    def __init__(self, api_key: str, timeout: int = 10, output_format: str = 'json'):
        super().__init__(api_key, timeout, output_format)

    def get_financials(
        self,
        symbol: str,
        statement: str,
        limit: int = 10,
        period: str = 'quarter',
        **query_params: Dict[str, Any]
    ) -> pd.DataFrame:
        """
        获取指定类型的财务报表数据。

        Args:
            symbol (str): 股票代码
            statement (str): 报表类型，可选值：'income', 'balance', 'cash', 'ratios', 'enterprise-value', 'key-metrics', 'financial-growth'
            limit (int): 限制返回的数据条数。
            period (str): 报表周期，'annual' 或 'quarter'。
            **query_params: 其他查询参数

        Returns:
            pd.DataFrame: 包含财务报表数据的DataFrame

        Raises:
            ValueError: 如果statement参数无效
        """
        # 映射报表类型到API端点
        endpoint_map = {
            "income": "income-statement",
            "balance": "balance-sheet-statement", 
            "cash": "cash-flow-statement"
        }

        if statement not in endpoint_map:
            raise ValueError(f"Invalid statement type: {statement}")

        # Combine direct parameters with query_params
        all_params = {"limit": limit, "period": period}
        all_params.update(query_params)

        # Use self._make_request for consistency
        res = self._make_request(f"{endpoint_map[statement]}/{symbol}", all_params)
        
        if not res:
            logger.warning(f"获取{symbol}的{statement}报表数据失败")
            return pd.DataFrame()

        return self._process_response(res)

    def get_merged_financials(self, symbol: str, limit: int = 40, period: str = 'quarter') -> Optional[pd.DataFrame]:
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
        income = self.get_financials(symbol, statement="income", period=period, limit=limit)
        balance = self.get_financials(symbol, statement="balance", period=period, limit=limit)
        cash = self.get_financials(symbol, statement="cash", period=period, limit=limit)

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
