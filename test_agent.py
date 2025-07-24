# -*- coding: utf-8 -*-
from pathlib import Path
import os
import sys
from dotenv import load_dotenv

# 添加项目根目录到Python路径
sys.path.insert(0, str(Path(__file__).parent))

from agno.agent import Agent
from agno.tools.python import PythonTools
from fmpxx import FMPClient

# 加载环境变量
load_dotenv()

def create_performance_visualization():
    """创建股票业绩可视化脚本"""
    
    # 获取API密钥
    api_key = os.getenv('FMP_KEY')
    if not api_key:
        raise ValueError("请设置FMP_KEY环境变量")
    
    # 创建FMP客户端
    client = FMPClient(api_key=api_key, output_format='pandas')
    
    # 获取AAPL的业绩数据
    symbol = "AAPL"
    performance_data = client.financials.get_stock_performance(symbol, limit=8, period='quarter')
    
    if performance_data is None or performance_data.empty:
        raise ValueError(f"无法获取{symbol}的业绩数据")
    
    # 准备数据用于可视化
    data_for_plot = performance_data[['period_date', 'revenue']].copy()
    data_for_plot['period_date'] = data_for_plot['period_date'].dt.strftime('%Y-%m')
    
    # 创建Python代理
    agent = Agent(
        tools=[PythonTools(base_dir=Path("tmp/python"))], 
        show_tool_calls=True
    )
    
    # 生成绘图脚本
    prompt = f"""
    请使用以下数据创建一个收入柱状图：
    
    数据：
    {data_for_plot.to_string(index=False)}
    
    要求：
    1. 使用matplotlib创建柱状图
    2. x轴显示period_date（格式：YYYY-MM）
    3. y轴显示revenue（单位：十亿美元）
    4. 标题："{symbol} 季度收入趋势"
    5. 旋转x轴标签45度以便阅读
    6. 添加网格线提高可读性
    7. 将revenue除以1e9转换为十亿美元单位
    8. 保存图表为png文件：{symbol}_revenue_chart.png
    9. 显示图表
    
    请提供完整的Python代码并执行。
    """
    
    print("正在生成收入柱状图...")
    agent.print_response(prompt)
    
    return data_for_plot

if __name__ == "__main__":
    try:
        data = create_performance_visualization()
        print(f"数据获取成功，共{len(data)}条记录")
        print("图表已生成并保存")
    except Exception as e:
        print(f"错误：{e}")