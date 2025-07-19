1. 核心设计原则 (Core Design Principles)
在开始写代码之前，我们先确立几个核心原则：

用户友好 (User-Friendly): API 调用应该直观、简单。用户不需要阅读 FMP 的每一个 API 文档细节就能使用。方法名和参数名应该清晰明了。

一致性 (Consistent): 库的接口风格保持一致。例如，所有获取时间序列数据的方法都应该接受相似的 start_date 和 end_date 参数。返回的数据格式也应该统一（例如，优先使用 Pandas DataFrame）。

健壮性 (Robust): 能够优雅地处理各种错误，如无效的 API 密钥、错误的股票代码、网络问题、API 速率限制等，并向用户返回有意义的错误信息。

高效性 (Efficient): 合理利用网络资源。例如，使用 requests.Session 来复用 TCP 连接，并考虑支持异步请求以提高并发性能。

文档完备 (Well-Documented): 每个公开的类和方法都应该有清晰的文档字符串 (docstrings)，解释其功能、参数和返回值。

2. 架构设计 (Architecture Design)
我建议采用面向对象的方法，围绕一个核心的 Client 类来构建。

2.1. 主客户端类 (FMPClient)
这是用户与库交互的主要入口。

初始化 (__init__):

接收用户的 api_key 作为核心参数。

可以接收可选参数，如 timeout (请求超时) 或 output_format (默认返回格式，如 'pandas' 或 'json')。

在内部，初始化一个 requests.Session 对象。将 API 密钥添加到会话的 params 中，这样后续所有请求都会自动带上 apikey=YOUR_KEY。

模块化/分类的属性 (Categorized Properties): FMP 的 API 数量众多，可以按照官方文档的分类将功能分组。例如：

client.stocks

client.forex

client.cryptocurrencies

client.company_fundamentals

client.market_data

这样做的好处是代码结构清晰，易于扩展，并且用户可以通过 "自动补全" 功能轻松发现可用的 API。

2.2. API 分类模块 (Endpoint Categories)
每个分类（如 financials）是一个类，它持有对主 Client 实例的引用，以便能发起网络请求。

示例: Financials 类:

该类包含与公司基本面相关的所有方法，如：

get_financials(statement='income',symbol=ticker, limit=4)

get_financials(statement='balance',symbol=ticker, limit=4)

get_financials(statement='cash',symbol=ticker, limit=4)


2.3. 底层请求处理器 (Request Handler)
在 FMPClient 内部，应该有一个私有的 _make_request 方法。所有公开的 API 调用方法最终都通过它来发送 HTTP 请求。

_make_request(endpoint, params=None):

构建 URL: 将基础 URL (https://financialmodelingprep.com/api/v3/) 和具体的 endpoint 拼接起来。

发送请求: 使用 self.session.get() 发送请求。

错误处理: 在这里集中处理 HTTP 错误。

200 OK: 请求成功。

401 Unauthorized: API 密钥无效，抛出自定义的 InvalidAPIKeyError。

404 Not Found: 股票代码或资源不存在，返回 None 或抛出 SymbolNotFoundError。

其他错误（如 429 Too Many Requests）: 抛出相应的 FMPAPIError。

解析响应: 将返回的 JSON 数据解析出来。

2.4. 数据格式化 (Data Formatting)
Pandas DataFrame: 对于表格和时间序列数据，Pandas DataFrame 是最理想的格式。它在金融数据分析领域是标准工具。你的方法应该能将 FMP 返回的 JSON 列表直接转换为结构化的 DataFrame。

原生 JSON: 对于一些简单的键值对响应（如公司简介），可以直接返回 Python 字典。

1. 核心组件代码示例
下面我们用代码来描绘这个设计。

3.1. 项目结构
fmp-python/
├── fmpxx/
│   ├── __init__.py         # 主入口，定义 FMPClient
│   ├── base.py             # 基类和请求处理器
│   ├── financials.py # 公司基本面模块
│   ├── stocks.py           # 股票数据模块
│   └── exceptions.py       # 自定义异常
├── tests/
│   └── ...                 # 测试代码
├── pyproject.toml          # 项目配置 (或 setup.py)
└── README.md
3.2 使用 uv 来管理和发布 Python 库