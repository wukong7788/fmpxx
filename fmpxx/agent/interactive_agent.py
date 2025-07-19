import os
import dotenv
import json
import pandas as pd
import sys
# 获取项目根目录的绝对路径
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# 将项目根目录添加到 Python 模块搜索路径
sys.path.append(project_root)
from fmpxx import FMPClient
from fmpxx.exceptions import FMPAPIError, InvalidAPIKeyError, SymbolNotFoundError, RateLimitExceededError, FMPConnectionError

# --- Gemini API Integration Placeholder ---
# In a real application, you would install the Google Generative AI SDK:
# pip install google-generativeai
# import google.generativeai as genai
# from google.generativeai.types import Tool

# Load environment variables
dotenv.load_dotenv()
API_KEY = os.getenv("FMP_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") # You would set this in your .env file

if not API_KEY:
    print("Error: FMP_KEY environment variable not set. Please set it in your .env file or environment.")
    exit(1)

# if not GEMINI_API_KEY:
#     print("Error: GEMINI_API_KEY environment variable not set. Please set it in your .env file or environment.")
#     exit(1)

client = FMPClient(api_key=API_KEY, output_format='pandas')

# Define tool specifications for Gemini (using google.generativeai.types.Tool format)
# These descriptions and parameters are crucial for the LLM to understand how to use your functions.
TOOLS = [
    # Tool for get_financials
    # Tool(function_declaration={
    #     "name": "get_financials",
    #     "description": "获取指定类型的财务报表数据，如损益表、资产负债表、现金流量表。",
    #     "parameters": {
    #         "type": "object",
    #         "properties": {
    #             "symbol": {"type": "string", "description": "股票代码，例如 'AAPL'"},
    #             "statement": {"type": "string", "enum": ["income", "balance", "cash"], "description": "报表类型，可选值：'income', 'balance', 'cash'"},
    #             "limit": {"type": "integer", "description": "限制返回的数据条数，默认为 10"},
    #             "period": {"type": "string", "enum": ["annual", "quarter"], "description": "报表周期，'annual' 或 'quarter'，默认为 'quarter'"}
    #         },
    #         "required": ["symbol", "statement"]
    #     }
    # }),
    # Tool for historical_price_full
    # Tool(function_declaration={
    #     "name": "historical_price_full",
    #     "description": "获取股票的完整历史日价格数据。",
    #     "parameters": {
    #         "type": "object",
    #         "properties": {
    #             "symbol": {"type": "string", "description": "股票代码，例如 'GOOG'"},
    #             "start": {"type": "string", "description": "开始日期，格式 YYYY-MM-DD"},
    #             "end": {"type": "string", "description": "结束日期，格式 YYYY-MM-DD"},
    #             "period": {"type": "integer", "description": "获取最近 N 年的数据，优先于 start/end"}
    #         },
    #         "required": ["symbol"]
    #     }
    # }),
    # Tool for quote
    # Tool(function_declaration={
    #     "name": "quote",
    #     "description": "获取股票的实时报价。",
    #     "parameters": {
    #         "type": "object",
    #         "properties": {
    #             "symbol": {"type": "string", "description": "股票代码，例如 'MSFT'"}
    #         },
    #         "required": ["symbol"]
    #     }
    # }),
    # Tool for search
    # Tool(function_declaration={
    #     "name": "search",
    #     "description": "根据查询字符串搜索公司或股票。",
    #     "parameters": {
    #         "type": "object",
    #         "properties": {
    #             "query": {"type": "string", "description": "搜索关键词，例如 'Tesla'"},
    #             "exchange": {"type": "string", "description": "交易所代码，例如 'NASDAQ'"},
    #             "limit": {"type": "integer", "description": "限制返回结果的数量，默认为 10"}
    #         },
    #         "required": ["query"]
    #     }
    # }),
    # Tool for get_merged_financials
    # Tool(function_declaration={
    #     "name": "get_merged_financials",
    #     "description": "获取合并后的财务报表（损益表、资产负债表、现金流量表）。",
    #     "parameters": {
    #         "type": "object",
    #         "properties": {
    #             "symbol": {"type": "string", "description": "股票代码，例如 'AMZN'"},
    #             "limit": {"type": "integer", "description": "限制返回的数据条数，默认为 40"},
    #             "period": {"type": "string", "enum": ["annual", "quarter"], "description": "报表周期，'annual' 或 'quarter'，默认为 'quarter'"}
    #         },
    #         "required": ["symbol"]
    #     }
    # }),
    # Tool for daily_prices
    # Tool(function_declaration={
    #     "name": "daily_prices",
    #     "description": "获取股票的每日历史价格（线形图）。",
    #     "parameters": {
    #         "type": "object",
    #         "properties": {
    #             "symbol": {"type": "string", "description": "股票代码，例如 'IBM'"},
    #             "start": {"type": "string", "description": "开始日期，格式 YYYY-MM-DD"},
    #             "end": {"type": "string", "description": "结束日期，格式 YYYY-MM-DD"},
    #             "period": {"type": "integer", "description": "获取最近 N 年的数据，优先于 start/end"}
    #         },
    #         "required": ["symbol"]
    #     }
    # })
]

def execute_tool(tool_name: str, **kwargs):
    """
    工具执行器，根据工具名称调用 fmpxx 库中的相应函数。
    """
    print(f"\n--- 调用工具: {tool_name}，参数: {kwargs} ---")
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

def get_gemini_model():
    """
    初始化 Gemini 模型并注册工具。
    你需要在这里替换为实际的 Gemini API 初始化代码。
    """
    # genai.configure(api_key=GEMINI_API_KEY)
    # model = genai.GenerativeModel(model_name='gemini-2.5-flash', tools=TOOLS)
    # return model
    print("Gemini 模型初始化占位符：请替换为实际的 Gemini API 初始化代码。")
    return None # Placeholder

def main():
    print("欢迎使用 AI 财务数据代理！")
    print("输入 'exit' 退出。")

    # model = get_gemini_model() # Uncomment in real implementation
    # if model is None: # Placeholder check
    #     print("无法初始化 Gemini 模型，请检查 API 密钥和网络连接。")
    #     return

    # chat = model.start_chat(enable_automatic_function_calling=True) # For automatic function calling

    while True:
        user_input = input("\n您好，有什么可以帮助您的？ > ").strip()

        if user_input.lower() == 'exit':
            print("再见！")
            break

        # --- Gemini API Interaction Placeholder ---
        # try:
        #     # Send user message to Gemini
        #     response = chat.send_message(user_input)
        #
        #     # Check if Gemini wants to call a tool
        #     if response.candidates[0].content.parts[0].function_call:
        #         tool_call = response.candidates[0].content.parts[0].function_call
        #         tool_name = tool_call.name
        #         tool_args = {k: v for k, v in tool_call.args.items()}
        #
        #         # Execute the tool
        #         tool_output = execute_tool(tool_name, **tool_args)
        #
        #         # Send tool output back to Gemini for a natural language response
        #         final_response = chat.send_message(tool_output)
        #         print(final_response.text)
        #     else:
        #         # If Gemini doesn't call a tool, it provides a text response
        #         print(response.text)
        #
        # except Exception as e:
        #     print(f"与 Gemini 交互时发生错误: {e}")
        #     print("请检查您的 Gemini API 密钥和网络连接，或尝试其他查询。")

        # --- Fallback for demonstration without actual Gemini API ---
        print("\n--- 模拟 Gemini 响应 (请替换为实际的 Gemini API 调用) ---")
        print("用户输入: ", user_input)
        print("如果这里是 Gemini，它会根据您的输入决定是否调用工具。")
        print("例如，如果您输入 '获取苹果的损益表'，Gemini 可能会决定调用 get_financials(symbol='AAPL', statement='income')")
        print("请手动模拟一个函数调用，例如: call_get_financials(symbol='AAPL', statement='income')")
        
        # This part remains for manual testing of tool execution
        tool_name, params = parse_user_input(user_input)
        if tool_name:
            if tool_name in [spec["function_declaration"]["name"] for spec in TOOLS]: # Check against actual tool names
                result = execute_tool(tool_name, **params)
                print("\n--- 工具执行结果 (模拟) ---")
                print(result)
            else:
                print(f"错误: 未知的工具名称 '{tool_name}'. 请检查输入格式或输入 'help' 查看可用工具。")
        else:
            print(params)

if __name__ == "__main__":
    main()
