## Changelog

### [0.3.4] - 2025-08-01
- 🆕 **新增收入细分数据功能**
  - 新增 `Financials.revenue_by_segment()` 方法，支持按地理区域或产品类别获取收入细分数据
  - 支持灵活的输出格式：`json` 或 `pandas` DataFrame
  - 优化数据结构：返回 DataFrame 格式时，日期为行，业务段为列（Mac、Service、iPhone 等）
- 🔧 **API 增强**
  - 使用 FMP v4 API 端点获取更高质量的收入细分数据
  - 新增 `_convert_segment_data_to_df()` 辅助方法处理嵌套 JSON 转换
- 📊 **使用方法**
  ```python
  # JSON 格式（默认）
  json_data = client.financials.revenue_by_segment('AAPL')
  
  # DataFrame 格式
  df = client.financials.revenue_by_segment('AAPL', output_format='pandas')
  ```

### [0.3.3] - 2025-07-31
- 🧹 **代码清理和重构**
  - 移除已废弃的 AI Agent 功能（基于 Agno 框架的交互式代理）
  - 优化测试文件结构，将数据文件移至 `tests/test_data/` 目录
  - 更新 `.gitignore` 忽略测试数据文件
- 📦 **项目结构优化**
  - 标准化测试输出路径，所有生成的 CSV 和 HTML 文件统一保存到 `tests/test_data/`
  - 清理项目根目录，移除临时测试文件
- 🔧 **依赖项更新**
  - 保持 AI Agent 功能完整，支持 agno 框架
  - 更新测试文件路径配置

### [0.3.2] - 2025-07-31
- 🆕 **新增股票业绩指标功能**
  - 新增 `Financials.get_stock_performance()` 方法，提供关键业绩指标
  - 包含营收(revenue)及增长率、毛利率(grossProfitRatio)、EPS及增长率
  - 提供运营利润率(operatingIncomeRatio)和自由现金流利润率(freeCashFlowMargin)
- 📊 **自由现金流利润率计算**
  - 公式：`freeCashFlowMargin = freeCashFlow / revenue`
  - 当API未提供自由现金流时，自动计算：`freeCashFlow = netCashProvidedByOperatingActivities + capitalExpenditure`
- 🗓️ **增强数据展示**
  - 新增 `calendarYear` 和 `period` 列，便于时间序列分析
  - 按日期降序排列，最新季度在前

### [0.3.1] - 2025-07-30
- 🔄 **Migrated from phidata to Agno framework**
  - Updated all imports from `phi` to `agno`
  - Replaced `phidata` dependency with `agno>=1.0.0`
  - Updated Google Gemini integration to use `google-genai>=1.26.0`
  - All AI Agent functionality preserved with improved performance
- 🧠 **AI Agent functionality** (`fmpxx.agent`) now based on Agno framework
  - Natural language understanding for financial queries (Chinese & English)
  - Intelligent function calling using Gemini 2.5 Flash model
  - Support for stock data (K-line, historical prices, quotes)
  - Support for financial statements (income, balance sheet, cash flow)
- 📦 **Package restructure** for PyPI compatibility
  - Moved AI agent to `fmpxx/fmpxx/agent/` directory
  - Added `create_agent()` factory function to main package
  - Fixed circular import issues
- 🔧 **Dependencies update**: Added `agno`, `google-genai`, `pydantic`
- 📝 **Updated documentation** with AI Agent usage examples

### [0.2.8] - 2025-07-29
- Added interactive AI Agent simulator (`fmpxx/agent/interactive_agent.py`) to demonstrate natural language interaction with the library.
- Updated `README.md` with instructions for the AI Agent simulator.

### [0.2.7] - 2025-07-28
- Refactored `financials.py`:
    - Consolidated specific financial statement methods (income, balance, cash flow, ratios, enterprise value, key metrics, growth metrics) into a single, more flexible `get_financials` function.
    - Optimized `get_financials` to leverage `_process_response` for consistent Pandas DataFrame conversion and column cleaning.
    - Updated `get_merged_financials` to use the new `get_financials` signature and incorporate robust data merging and cleaning logic.
- Renamed `company_fundamentals.py` to `financials.py` and updated all references.
- Updated `README.md` and `tests.py` to reflect the new API structure and usage.
- Enhanced Pandas display options in `tests.py` for better output readability.