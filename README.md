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

# 获取股票数据
print("\n--- Stocks Data ---")
historical_prices = client.stocks.historical_price_full("AAPL", from_date="2023-01-01", to_date="2023-01-05")
print("Historical Prices (first 5 rows):\n", historical_prices.head())

stock_list = client.stocks.stock_list()
print("Stock List (first 5 rows):\n", stock_list.head())

quote = client.stocks.quote("AAPL")
print("Quote:\n", quote)

search_results = client.stocks.search(query='Apple', limit=2)
print("Search Results (first 2 rows):\n", search_results.head())
```

## AI Agent 示例

`fmpxx/agent/interactive_agent.py` 文件提供了一个模拟的 AI 代理，演示了如何通过自然语言（模拟的函数调用格式）与 `fmpxx` 库进行交互。这个示例展示了如何将用户意图映射到库中的函数，并执行这些函数以获取数据。

**运行 AI Agent 模拟器：**

1.  确保你已安装所有依赖项并激活了虚拟环境。
2.  运行以下命令启动模拟器：

    ```bash
    source .venv/bin/activate
    python fmpxx/agent/interactive_agent.py
    ```

3.  在模拟器中，你可以输入 `help` 查看所有可用的工具及其参数。
4.  按照 `call_tool_name(param1=value1, param2=value2)` 的格式输入命令来模拟 AI 代理的函数调用。

**示例命令：**

*   `call_get_financials(symbol='AAPL', statement='income', limit=1, period='quarter')`
*   `call_historical_price_full(symbol='GOOG', period=5)`
*   `call_quote(symbol='MSFT')`
*   `call_search(query='Tesla', exchange='NASDAQ')`
*   `call_get_merged_financials(symbol='AMZN')`
*   `call_daily_prices(symbol='IBM', start='2023-01-01', end='2023-01-31')`

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