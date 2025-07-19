核心需求：

构建一个基于 phidata 框架 的 AI Agent，该 Agent 能够：

理解自然语言查询： 准确解析用户关于股票K线数据（例如，历史价格、交易量）和财务数据（例如，资产负债表、利润表、现金流量表）的自然语言请求。

智能函数调用： 根据用户查询，自动识别并调用 fmpxx 库中 financials.py 和 stocks.py 模块里最匹配的函数。

数据检索与返回： 利用 fmpxx 函数获取相应的金融数据，并将结果以清晰、易懂的格式返回给用户。

关键组成部分和技术栈：

Agent 框架： phidata (作为主要的 Agent 开发框架)

LLM 交互： 代理将利用一个 大型语言模型 (LLM) 来理解用户意图并决定调用哪个 fmpxx 函数。

数据源/工具层： fmpxx 库 (具体是 financials.py 和 stocks.py 模块)

项目结构： fin_ai_agent 将位于项目的 agent/ 目录下。

具体期望行为：

示例1（K线数据）：

用户提问： "帮我查一下苹果公司（AAPL）最近5天的日K线数据。"

Agent 行为： LLM 解析请求 -> Agent 调用 fmpxx.stocks 中的相关函数（例如 get_daily_kline 或类似函数，如果存在） -> 返回AAPL最近5天的K线数据。

示例2（财务数据）：

用户提问： "特斯拉（TSLA）最新的年度资产负债表是什么？"

Agent 行为： LLM 解析请求 -> Agent 调用 fmpxx.financials 中的相关函数（例如 get_balance_sheet 或类似函数） -> 返回TSLA最新的年度资产负债表。

phidata 特性利用：

利用 phidata 的 工具集成 能力，将 fmpxx 库中的函数封装为 Agent 可调用的工具。

利用 phidata 的 Agent 定义和编排 能力，构建一个能够理解、规划和执行任务的金融分析 Agent。

以上的示例卸载 fmpxx/test_agent.py 文件中