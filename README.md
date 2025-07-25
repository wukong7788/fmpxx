# fmpxx - Financial Modeling Prep Python SDK

fmpxx 是一个用于访问 Financial Modeling Prep (FMP) API 的 Python SDK，提供了简单易用的接口来获取金融市场数据。

## 功能特点

- 📈 实时股票报价数据
- 💼 公司财务报表（损益表、资产负债表、现金流量表）
- 📊 历史股价数据
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
from fmpxx import FMPClient

# 初始化客户端
api_key = "your_api_key"
client = FMPClient(api_key, output_format='pandas')

# 获取公司基本面数据
print("--- Financials ---")
income_statement = client.financials.get_financials("AAPL", statement="income", limit=1)
print("Income Statement (first row):\n", income_statement.head(1))

balance_sheet = client.financials.get_financials("AAPL", statement="balance", limit=1)
print("Balance Sheet (first row):\n", balance_sheet.head(1))

cash_flow_statement = client.financials.get_financials("AAPL", statement="cash", limit=1)
print("Cash Flow Statement (first row):\n", cash_flow_statement.head(1))

merged_financials = client.financials.get_merged_financials("AAPL", limit=1)
print("Merged Financials (first row):\n", merged_financials.head(1))

# 获取股票关键业绩指标
print("\n--- Stock Performance Analysis ---")
performance = client.financials.get_stock_performance("AAPL", limit=8)
print("Key Performance Metrics (first 3 quarters):\n", performance.head(3))

# 自由现金流利润率计算公式说明
print("\n自由现金流利润率计算公式:")
print("freeCashFlowMargin = freeCashFlow / revenue")
print("当API未提供自由现金流时，使用: freeCashFlow = netCashProvidedByOperatingActivities + capitalExpenditure")
historical_prices = client.stocks.historical_price_full("AAPL", from_date="2023-01-01", to_date="2023-01-05")
print("Historical Prices (first 5 rows):\n", historical_prices.head())

stock_list = client.stocks.stock_list()
print("Stock List (first 5 rows):\n", stock_list.head())

quote = client.stocks.quote("AAPL")
print("Quote:\n", quote)

search_results = client.stocks.search(query='Apple', limit=2)
print("Search Results (first 2 rows):\n", search_results.head())
```

## AI Agent 功能 🧠

fmpxx 现在集成了基于 **Agno** 框架的 AI Agent，支持自然语言查询！

### 功能特点
- 🎯 **自然语言理解**：理解中文和英文的金融数据查询
- 🔍 **智能函数调用**：自动识别并调用正确的 fmpxx 函数
- 📊 **多数据类型支持**：
  - 股票K线数据（历史价格、交易量）
  - 公司财务报表（资产负债表、利润表、现金流量表）
  - 实时股价和搜索功能

### 快速开始

```python
from fmpxx import create_agent

# 创建 AI Agent
agent = create_agent()

# 自然语言查询
response = agent.query("帮我查一下苹果公司（AAPL）最近5天的日K线数据")
print(response)

# 中文查询示例
response = agent.query("特斯拉（TSLA）最新的年度资产负债表是什么？")
print(response)

# 英文查询示例
response = agent.query("What's Google's current stock price?")
print(response)
```

### 环境配置

创建 `.env` 文件：
```
FMP_KEY=your_fmp_api_key
GEMINI_API_KEY=your_google_gemini_key
```

### 运行测试脚本

```bash
# 测试单个查询
uv run python test_agent.py "帮我查一下苹果公司（AAPL）最近5天的日K线数据"

# 交互式聊天模式
uv run python test_agent.py --chat
```

### 支持的自然语言示例

**股票数据：**
- "帮我查一下苹果公司（AAPL）最近5天的日K线数据"
- "Google过去一个月的历史股价"
- "微软当前股价是多少？"

**财务数据：**
- "特斯拉（TSLA）最新的年度资产负债表是什么？"
- "亚马逊最新的季度利润表"
- "Facebook的现金流量表"

**搜索功能：**
- "搜索包含'半导体'的公司"
- "查找科技行业的股票"

## API 文档

### FMPClient 类

这是用户与库交互的主要入口。它通过 `api_key` 初始化，并提供对不同数据类别的访问。

#### 初始化参数：
- `api_key` (str): 您的 FMP API 密钥。
- `timeout` (int, optional): 请求超时时间（秒）。默认为 10。
- `output_format` (str, optional): 期望的输出格式（`'json'` 或 `'pandas'`）。默认为 `'json'`。

#### 属性：
- `financials` (Financials): 访问公司基本面数据，如损益表、资产负债表、现金流量表、财务比率等。
- `stocks` (Stocks): 访问股票市场数据，如历史价格、实时报价、股票列表和搜索功能。

### Financials 类

提供访问 FMP 公司基本面 API 端点的方法。通常通过 `FMPClient.financials` 属性访问。

#### 主要方法：
- `get_financials(symbol, statement, limit=10, period='quarter', **query_params)`: 获取指定类型的财务报表数据（如收入报表、资产负债表、现金流量表）。
- `get_merged_financials(symbol, limit=40, period='quarter')`: 合并现金流量表、损益表和资产负债表三张财务报表。
- `get_stock_performance(symbol, limit=8, period='quarter')`: 获取股票关键业绩指标，包括营收增长率、毛利率、EPS增长率、运营利润率和自由现金流利润率。

#### 自由现金流利润率计算
- **公式**: `freeCashFlowMargin = freeCashFlow / revenue`
- **备用计算**（当API未提供自由现金流时）：
  ```
  freeCashFlow = netCashProvidedByOperatingActivities + capitalExpenditure
  ```
- **返回数据**: 包含calendarYear、period、revenue、revenue_growth_rate、grossProfitRatio、eps、eps_growth_rate、operatingIncomeRatio、freeCashFlowMargin

### Stocks 类

提供访问 FMP 股票 API 端点的方法。通常通过 `FMPClient.stocks` 属性访问。

#### 主要方法：
- `historical_price_full(symbol, series_type=None, from_date=None, to_date=None)`: 获取股票的完整历史日价格。
- `daily_prices(symbol, start=None, end=None, period=None)`: 获取股票的历史日价格（线形图）。
- `stock_list()`: 获取所有可用股票的列表。
- `quote(symbol)`: 获取给定股票的实时报价。
- `search(query, exchange=None, limit=10)`: 按名称或符号搜索公司。

## 贡献指南

欢迎贡献代码！请遵循以下步骤：

1. Fork 本项目
2. 创建新的分支 (`git checkout -b feature/YourFeature`)
3. 提交更改 (`git commit -m 'Add some feature'`)
4. 推送到分支 (`git push origin feature/YourFeature`)
5. 创建 Pull Request

## 许可证

本项目采用 MIT 许可证。详情请见 LICENSE 文件。