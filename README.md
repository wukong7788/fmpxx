# 0.2.1
分成了quote, financials, util三个类

# fmpxx

fmpxx 是一个用于获取和处理金融市场数据的 Python 库，基于 Financial Modeling Prep (FMP) API。

## 功能特点

- 获取股票报价数据
- 获取公司财务报表
- 获取历史股价数据
- 计算市盈率 (PE) 和每股收益 (EPS)
- 支持数据可视化

## 安装

使用 pip 安装 fmpxx：

## 主要的类

### Quote

Quote 类用于获取和处理股票报价数据。

### Financials

Financials 类用于获取和处理公司财务报表数据。

### Util

Util 类包含一些常用的工具函数，如计算市盈率 (PE) 和每股收益 (EPS)。

## 使用示例     

```python
from fmpxx.quote import Quote
from fmpxx.financials import Financials
from fmpxx.util import Util

# 获取股票报价数据
quote = Quote("your_api_key")
quote_data = quote.get_full_quote("AAPL")

# 获取公司财务报表数据
financials = Financials("your_api_key")
income_statement = financials.get_income_statement("AAPL")

