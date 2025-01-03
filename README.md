# fmpxx - Financial Modeling Prep Python SDK
uv 是最新，最符合人类的 python 环境和包管理工具，速度也非常快，强烈建议使用！！！
https://github.com/astral-sh/uv
fmpxx 是一个用于访问 Financial Modeling Prep (FMP) API 的 Python SDK，提供了简单易用的接口来获取金融市场数据。

## 功能特点

- 📈 实时股票报价数据
- 💼 公司财务报表（损益表、资产负债表、现金流量表）
- 📊 历史股价数据
- 📰 股票新闻和分析师预测
- 📊 S&P 500 成分股数据
- 🔄 自动重试机制和错误处理
- 🐼 数据返回为 Pandas DataFrame，便于分析

## 安装

建议使用 [uv](https://github.com/astral-sh/uv) 管理 Python 环境：

```bash
# 1. 安装uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. 创建虚拟环境
uv venv

# 3. 安装依赖
uv install .
```

## 快速开始

```python
from fmpxx import FMPClient, Quote, Financials, Info

# 初始化客户端
api_key = "your_api_key"
client = FMPClient(api_key)

# 获取股票报价
quote = Quote(api_key)
aapl_quote = quote.get_full_quote("AAPL")

# 获取财务报表
financials = Financials(api_key)
income_statement = financials.get_income_statement("AAPL")

# 获取股票新闻
info = Info(api_key)
news = info.get_stock_news(["AAPL", "MSFT"], period=7)
```

## API 文档

### FMPClient 类

基础客户端类，提供API请求和响应处理功能。

#### 主要方法：
- `_handle_response(endpoint, params)`：处理API请求和响应
- `trans_to_df(res)`：将API响应转换为DataFrame

### Quote 类

获取股票报价数据。

#### 主要方法：
- `get_simple_quote(symbol)`：获取简单报价
- `get_full_quote(symbol)`：获取完整报价
- `get_his_daily(symbol, period)`：获取历史日线数据

### Financials 类

获取公司财务报表数据。

#### 主要方法：
- `get_financials(symbol, statement)`：获取指定类型财务报表
- `get_merged_financials(symbol)`：合并三张财务报表
- `get_8k_update()`：获取8-K报告更新
- `get_sec_update(days)`：获取SEC更新
- `get_income_statement(symbol)`：获取收益报表
- `get_earnings_his(symbol, period)`：获取历史盈利日历

### Info 类

获取非行情、非财务数据。

#### 主要方法：
- `get_stock_news(symbols, period)`：获取股票新闻
- `get_analyst_estimates(symbol)`：获取分析师预测
- `sp500_constituent()`：获取当前S&P 500成分股
- `sp500_his_list()`：获取历史和当前S&P 500成分股
- `get_tickers()`：获取股票列表
- `get_available_tickers()`：获取可交易证券列表



## 许可证

本项目采用 MIT 许可证。详情请见 LICENSE 文件。

## 版本历史
### 0.2.5
重新整理了 client，quote，financials 几个文件的分工

### 0.2.2
- 增加了财报日 close change 的数据

### 0.2.1
- 将功能模块化为 quote, financials, util 三个类
