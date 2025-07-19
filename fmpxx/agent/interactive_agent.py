import os
import dotenv
import json
import pandas as pd
from fmpxx import FMPClient
from fmpxx.exceptions import FMPAPIError, InvalidAPIKeyError, SymbolNotFoundError, RateLimitExceededError, FMPConnectionError

# Load environment variables
dotenv.load_dotenv()
API_KEY = os.getenv("FMP_KEY")

if not API_KEY:
    print("Error: FMP_KEY environment variable not set. Please set it in your .env file or environment.")
    exit(1)

client = FMPClient(api_key=API_KEY, output_format='pandas')

# Define tool specifications (simplified for demonstration)
# In a real LLM integration, these would be provided to the LLM's function calling API
TOOL_SPECS = {
    "get_financials": {
        "description": "获取指定类型的财务报表数据，如损益表、资产负债表、现金流量表。",
        "parameters": {
            "type": "object",
            "properties": {
                "symbol": {"type": "string", "description": "股票代码，例如 'AAPL'"},
                "statement": {"type": "string", "enum": ["income", "balance", "cash"], "description": "报表类型，可选值：'income', 'balance', 'cash'"},
                "limit": {"type": "integer", "description": "限制返回的数据条数，默认为 10"},
                "period": {"type": "string", "enum": ["annual", "quarter"], "description": "报表周期，'annual' 或 'quarter'，默认为 'quarter'"}
            },
            "required": ["symbol", "statement"]
        }
    },
    "historical_price_full": {
        "description": "获取股票的完整历史日价格数据。",
        "parameters": {
            "type": "object",
            "properties": {
                "symbol": {"type": "string", "description": "股票代码，例如 'GOOG'"},
                "start": {"type": "string", "description": "开始日期，格式 YYYY-MM-DD"},
                "end": {"type": "string", "description": "结束日期，格式 YYYY-MM-DD"},
                "period": {"type": "integer", "description": "获取最近 N 年的数据，优先于 start/end"}
            },
            "required": ["symbol"]
        }
    },
    "quote": {
        "description": "获取股票的实时报价。",
        "parameters": {
            "type": "object",
            "properties": {
                "symbol": {"type": "string", "description": "股票代码，例如 'MSFT'"}
            },
            "required": ["symbol"]
        }
    },
    "search": {
        "description": "根据查询字符串搜索公司或股票。",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "搜索关键词，例如 'Tesla'"},
                "exchange": {"type": "string", "description": "交易所代码，例如 'NASDAQ'"},
                "limit": {"type": "integer", "description": "限制返回结果的数量，默认为 10"}
            },
            "required": ["query"]
        }
    },
    "get_merged_financials": {
        "description": "获取合并后的财务报表（损益表、资产负债表、现金流量表）。",
        "parameters": {
            "type": "object",
            "properties": {
                "symbol": {"type": "string", "description": "股票代码，例如 'AMZN'"},
                "limit": {"type": "integer", "description": "限制返回的数据条数，默认为 40"},
                "period": {"type": "string", "enum": ["annual", "quarter"], "description": "报表周期，'annual' 或 'quarter'，默认为 'quarter'"}
            },
            "required": ["symbol"]
        }
    },
    "daily_prices": {
        "description": "获取股票的每日历史价格（线形图）。",
        "parameters": {
            "type": "object",
            "properties": {
                "symbol": {"type": "string", "description": "股票代码，例如 'IBM'"},
                "start": {"type": "string", "description": "开始日期，格式 YYYY-MM-DD"},
                "end": {"type": "string", "description": "结束日期，格式 YYYY-MM-DD"},
                "period": {"type": "integer", "description": "获取最近 N 年的数据，优先于 start/end"}
            },
            "required": ["symbol"]
        }
    }
}

def execute_tool(tool_name: str, **kwargs):
    """
    模拟工具执行器，根据工具名称调用 fmpxx 库中的相应函数。
    """
    print(f"\n--- 模拟调用工具: {tool_name}，参数: {kwargs} ---")
    try:
        if tool_name == "get_financials":
            result = client.financials.get_financials(**kwargs)
        elif tool_name == "historical_price_full":
            result = client.stocks.historical_price_full(**kwargs)
        elif tool_name == "quote":
            result = client.stocks.quote(**kwargs)
        elif tool_name == "search":
            result = client.stocks.search(**kwargs)
        elif tool_name == "get_merged_financials":
            result = client.financials.get_merged_financials(**kwargs)
        elif tool_name == "daily_prices":
            result = client.stocks.daily_prices(**kwargs)
        else:
            return f"错误: 未知的工具名称 {tool_name}"

        if isinstance(result, pd.DataFrame) and not result.empty:
            return result.to_string() # Convert DataFrame to string for display
        elif result is None or (isinstance(result, pd.DataFrame) and result.empty):
            return "未找到数据。"
        else:
            return str(result) # Convert other results to string

    except FMPAPIError as e:
        return f"API 错误: {e}"
    except Exception as e:
        return f"执行工具时发生意外错误: {e}"

def parse_user_input(user_input: str):
    """
    简化的用户输入解析器，模拟 LLM 的函数调用决策。
    用户需要输入类似 "call_tool_name(param1=value1, param2=value2)" 的格式。
    """
    user_input = user_input.strip()
    if not user_input.startswith("call_"):
        return None, "请以 'call_tool_name(param1=value1, ...)' 的格式输入命令，或输入 'help' 查看可用工具。"

    try:
        # Extract tool name and arguments string
        parts = user_input.split('(', 1)
        tool_name = parts[0].replace("call_", "")
        args_str = parts[1].rstrip(')')

        kwargs = {}
        if args_str:
            # Split arguments by comma, handle potential nested structures if needed (not implemented here)
            arg_pairs = args_str.split(',')
            for pair in arg_pairs:
                key, value = pair.split('=', 1)
                key = key.strip()
                value = value.strip()
                # Attempt to convert value to appropriate type
                if value.startswith("'" ) and value.endswith("'"):
                    kwargs[key] = value[1:-1]  # String
                elif value.lower() == 'true':
                    kwargs[key] = True
                elif value.lower() == 'false':
                    kwargs[key] = False
                elif value.isdigit():
                    kwargs[key] = int(value)  # Integer
                elif '.' in value and value.replace('.', '', 1).isdigit():
                    kwargs[key] = float(value) # Float
                elif value.lower() == 'none':
                    kwargs[key] = None
                else:
                    kwargs[key] = value # Fallback for other types

        return tool_name, kwargs
    except Exception as e:
        return None, f"解析输入时发生错误: {e}. 请检查输入格式。"

def display_help():
    print("\n--- 可用工具 (模拟 LLM 的工具列表) ---")
    for tool_name, spec in TOOL_SPECS.items():
        print(f"工具名称: {tool_name}")
        print(f"  描述: {spec['description']}")
        params = []
        for param_name, param_spec in spec['parameters']['properties'].items():
            param_type = param_spec['type']
            param_desc = param_spec['description']
            required = "(必需)" if param_name in spec['parameters'].get('required', []) else "(可选)"
            params.append(f"    - {param_name} ({param_type}) {required}: {param_desc}")
        print("\n".join(params))
        print("-" * 30)

def main():
    print("欢迎使用 AI 财务数据代理模拟器！")
    print("输入 'help' 查看可用命令和工具。")
    print("输入 'exit' 退出。")
    print("请以 'call_tool_name(param1=value1, param2=value2)' 的格式输入命令。")

    while True:
        user_input = input("\n您好，有什么可以帮助您的？ > ").strip()

        if user_input.lower() == 'exit':
            print("再见！")
            break
        elif user_input.lower() == 'help':
            display_help()
            continue

        tool_name, params = parse_user_input(user_input)

        if tool_name:
            if tool_name in TOOL_SPECS:
                result = execute_tool(tool_name, **params)
                print("\n--- 工具执行结果 ---")
                print(result)
            else:
                print(f"错误: 未知的工具名称 '{tool_name}'. 请输入 'help' 查看可用工具。")
        else:
            print(params) # params contains the error message from parse_user_input

if __name__ == "__main__":
    main()