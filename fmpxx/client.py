import logging
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import pandas as pd
from dotenv import load_dotenv, find_dotenv
from typing import Dict, Any, Optional, List, Union

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 配置Pandas显示选项
pd.set_option("expand_frame_repr", False)  # 当列太多时不换行
pd.set_option("display.max_rows", 5000)  # 最多显示数据的行数

# 加载环境变量
load_dotenv(find_dotenv())


class FMPClient:
    """
    FMP API客户端类，用于与Financial Modeling Prep API进行交互。

    Attributes:
        api_key (str): API密钥
        url (str): API基础URL
        timeout (int): 请求超时时间
        session (requests.Session): 请求会话对象
    """
    DEFAULT_HOST = "https://financialmodelingprep.com/api"

    def __init__(self, api_key: str, timeout: int = 10, max_retries: int = 3) -> None:
        """
        初始化FMPClient实例。

        Args:
            api_key (str): API密钥
            timeout (int): 请求超时时间，默认为10秒
            max_retries (int): 最大重试次数，默认为3次
        """
        self.api_key = api_key
        self.url = self.DEFAULT_HOST
        self.timeout = timeout
        self.session = self._create_session(max_retries)

    def _create_session(self, max_retries: int) -> requests.Session:
        """
        创建带有重试机制的请求会话。

        Args:
            max_retries (int): 最大重试次数

        Returns:
            requests.Session: 配置好的请求会话对象
        """
        session = requests.Session()
        retries = Retry(
            total=max_retries,
            backoff_factor=0.1,
            status_forcelist=[500, 502, 503, 504]
        )
        session.mount('https://', HTTPAdapter(max_retries=retries))
        return session

    def _handle_response(self, endpoint: str, params: Dict[str, Any]) -> Optional[Union[Dict, List]]:
        """
        处理API请求响应。

        Args:
            endpoint (str): API端点
            params (Dict[str, Any]): 请求参数

        Returns:
            Optional[Union[Dict, List]]: 解析后的JSON响应数据，请求失败时返回None
        """
        params['apikey'] = self.api_key
        try:
            response = self.session.get(endpoint, params=params, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"请求失败: {e}")
            return None

    @staticmethod
    def trans_to_df(res: Union[Dict[str, Any], List[Dict[str, Any]]]) -> pd.DataFrame:
        """
        将API响应转换为DataFrame。

        Args:
            res (Union[Dict[str, Any], List[Dict[str, Any]]]): API响应数据

        Returns:
            pd.DataFrame: 转换后的DataFrame，如果输入为空则返回空DataFrame
        """
        return pd.DataFrame(res) if res else pd.DataFrame()
