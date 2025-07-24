#!/usr/bin/env python3
"""
双轴可视化图表工具

功能：
1. 创建营收（柱状图）和营收增长率（折线图）双y轴图表
2. 创建营业利润（柱状图）和营业利润增长率（折线图）双y轴图表
3. 生成单个HTML文件展示所有双轴图表
"""

import sys
import os
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

# 添加项目根目录到路径
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

from fmpxx import FMPClient
import dotenv

def setup_client():
    """设置FMP客户端"""
    dotenv.load_dotenv()
    api_key = os.getenv("FMP_KEY")
    if not api_key:
        raise ValueError("FMP_KEY environment variable not set")
    return FMPClient(api_key=api_key, output_format='pandas')

def get_stock_performance_batch(client, symbols, limit=8):
    """
    批量获取股票业绩数据
    
    Args:
        client: FMPClient实例
        symbols: 股票代码列表
        limit: 获取的季度数
    
    Returns:
        dict: 股票代码到DataFrame的映射
    """
    results = {}
    
    for symbol in symbols:
        print(f"正在获取 {symbol} 的业绩数据...")
        try:
            df = client.financials.get_stock_performance(symbol=symbol, limit=limit)
            if df is not None and not df.empty:
                # 添加股票代码列用于后续分析
                df['symbol'] = symbol
                results[symbol] = df
                
                # 保存CSV
                csv_path = f'tests/performance_{symbol}.csv'
                df.to_csv(csv_path, index=False)
                print(f"✅ {symbol} 数据已保存到 {csv_path}")
            else:
                print(f"❌ 无法获取 {symbol} 的数据")
        except Exception as e:
            print(f"❌ 获取 {symbol} 数据时出错: {str(e)}")
    
    return results

def plot_revenue_dual_axis(data_dict):
    """
    创建营收（柱状图）和营收增长率（折线图）双y轴图表
    
    Args:
        data_dict: 股票代码到DataFrame的映射
    """
    if not data_dict:
        print("没有数据可供绘图")
        return
    
    fig = make_subplots(
        rows=len(data_dict), cols=1,
        subplot_titles=[f'{symbol} - 营收与增长率双轴图' for symbol in data_dict.keys()],
        vertical_spacing=0.1,
        specs=[[{"secondary_y": True}] for _ in range(len(data_dict))]
    )
    
    colors = px.colors.qualitative.Set1
    
    for i, (symbol, df) in enumerate(data_dict.items()):
        color = colors[i % len(colors)]
        df = df.sort_values('period_date')
        
        # 营收柱状图（左侧y轴）
        fig.add_trace(
            go.Bar(
                x=df['period_date'],
                y=df['revenue']/1e9,
                name=f'{symbol} 营收',
                marker_color=color,
                opacity=0.7,
                legendgroup=f'group_{symbol}',
                legendgrouptitle_text=f'{symbol}'
            ),
            row=i+1, col=1
        )
        
        # 营收增长率折线图（右侧y轴）
        fig.add_trace(
            go.Scatter(
                x=df['period_date'],
                y=df['revenue_growth_rate']*100,
                name=f'{symbol} 增长率',
                line=dict(color=color, width=3),
                mode='lines+markers',
                legendgroup=f'group_{symbol}'
            ),
            row=i+1, col=1,
            secondary_y=True
        )
    
    # 更新布局
    fig.update_layout(
        title='营收与营收增长率双轴对比分析',
        height=300 * len(data_dict),
        template='plotly_white',
        hovermode='x unified'
    )
    
    # 更新坐标轴标签
    for i in range(len(data_dict)):
        fig.update_yaxes(title_text="营收 (十亿美元)", row=i+1, col=1, secondary_y=False)
        fig.update_yaxes(title_text="营收增长率 (%)", row=i+1, col=1, secondary_y=True)
    
    fig.update_xaxes(title_text="报告期", row=len(data_dict), col=1)
    
    return fig

def plot_operating_income_dual_axis(data_dict):
    """
    创建营业利润（柱状图）和营业利润增长率（折线图）双y轴图表
    
    Args:
        data_dict: 股票代码到DataFrame的映射
    """
    if not data_dict:
        print("没有数据可供绘图")
        return
    
    fig = make_subplots(
        rows=len(data_dict), cols=1,
        subplot_titles=[f'{symbol} - 营业利润与增长率双轴图' for symbol in data_dict.keys()],
        vertical_spacing=0.1,
        specs=[[{"secondary_y": True}] for _ in range(len(data_dict))]
    )
    
    colors = px.colors.qualitative.Set2
    
    for i, (symbol, df) in enumerate(data_dict.items()):
        color = colors[i % len(colors)]
        df = df.sort_values('period_date')
        
        # 营业利润柱状图（左侧y轴）
        fig.add_trace(
            go.Bar(
                x=df['period_date'],
                y=df['operatingIncome']/1e9,
                name=f'{symbol} 营业利润',
                marker_color=color,
                opacity=0.7,
                legendgroup=f'group_{symbol}',
                legendgrouptitle_text=f'{symbol}'
            ),
            row=i+1, col=1
        )
        
        # 营业利润增长率折线图（右侧y轴）
        fig.add_trace(
            go.Scatter(
                x=df['period_date'],
                y=df['operatingIncome_growth_rate']*100,
                name=f'{symbol} 增长率',
                line=dict(color=color, width=3),
                mode='lines+markers',
                legendgroup=f'group_{symbol}'
            ),
            row=i+1, col=1,
            secondary_y=True
        )
    
    # 更新布局
    fig.update_layout(
        title='营业利润与增长率双轴对比分析',
        height=300 * len(data_dict),
        template='plotly_white',
        hovermode='x unified'
    )
    
    # 更新坐标轴标签
    for i in range(len(data_dict)):
        fig.update_yaxes(title_text="营业利润 (十亿美元)", row=i+1, col=1, secondary_y=False)
        fig.update_yaxes(title_text="营业利润增长率 (%)", row=i+1, col=1, secondary_y=True)
    
    fig.update_xaxes(title_text="报告期", row=len(data_dict), col=1)
    
    return fig

def generate_dual_axis_charts(data_dict):
    """
    生成包含所有双轴图表的HTML文件
    
    Args:
        data_dict: 股票代码到DataFrame的映射
    """
    if not data_dict:
        print("没有数据可供绘图")
        return
    
    # 创建营收双轴图表
    revenue_fig = plot_revenue_dual_axis(data_dict)
    
    # 创建营业利润双轴图表
    operating_income_fig = plot_operating_income_dual_axis(data_dict)
    
    # 保存为HTML文件
    revenue_fig.write_html('tests/revenue_dual_axis.html')
    operating_income_fig.write_html('tests/operating_income_dual_axis.html')
    
    # 创建组合图表
    combined_fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=(
            '营收与营收增长率双轴对比',
            '营业利润与营业利润增长率双轴对比'
        ),
        vertical_spacing=0.15,
        specs=[[{"secondary_y": True}], [{"secondary_y": True}]]
    )
    
    colors = px.colors.qualitative.Set1
    
    for i, (symbol, df) in enumerate(data_dict.items()):
        color = colors[i % len(colors)]
        df = df.sort_values('period_date')
        
        # 上半部分：营收双轴
        combined_fig.add_trace(
            go.Bar(
                x=df['period_date'],
                y=df['revenue']/1e9,
                name=f'{symbol} 营收',
                marker_color=color,
                opacity=0.7,
                legendgroup=f'revenue_{symbol}',
                showlegend=True
            ),
            row=1, col=1
        )
        
        combined_fig.add_trace(
            go.Scatter(
                x=df['period_date'],
                y=df['revenue_growth_rate']*100,
                name=f'{symbol} 营收增长率',
                line=dict(color=color, width=2),
                mode='lines+markers',
                legendgroup=f'revenue_{symbol}',
                showlegend=True
            ),
            row=1, col=1,
            secondary_y=True
        )
        
        # 下半部分：营业利润双轴
        combined_fig.add_trace(
            go.Bar(
                x=df['period_date'],
                y=df['operatingIncome']/1e9,
                name=f'{symbol} 营业利润',
                marker_color=color,
                opacity=0.7,
                legendgroup=f'profit_{symbol}',
                showlegend=True
            ),
            row=2, col=1
        )
        
        combined_fig.add_trace(
            go.Scatter(
                x=df['period_date'],
                y=df['operatingIncome_growth_rate']*100,
                name=f'{symbol} 营业利润增长率',
                line=dict(color=color, width=2, dash='dash'),
                mode='lines+markers',
                legendgroup=f'profit_{symbol}',
                showlegend=True
            ),
            row=2, col=1,
            secondary_y=True
        )
    
    # 更新组合图表布局
    combined_fig.update_layout(
        title='营收与营业利润双轴对比分析',
        height=800,
        template='plotly_white',
        hovermode='x unified',
        barmode='group'  # 确保柱状图可以并排显示
    )
    
    combined_fig.update_yaxes(title_text="营收 (十亿美元)", row=1, col=1, secondary_y=False)
    combined_fig.update_yaxes(title_text="营收增长率 (%)", row=1, col=1, secondary_y=True)
    combined_fig.update_yaxes(title_text="营业利润 (十亿美元)", row=2, col=1, secondary_y=False)
    combined_fig.update_yaxes(title_text="营业利润增长率 (%)", row=2, col=1, secondary_y=True)
    combined_fig.update_xaxes(title_text="报告期", row=2, col=1)
    
    combined_fig1.write_html('tests/dual_axis_combined.html')
    combined_fig2.write_html('tests/dual_axis_profit.html')
    
    print("📊 双轴图表已生成:")
    print("   - tests/revenue_dual_axis.html")
    print("   - tests/operating_income_dual_axis.html")
    print("   - tests/dual_axis_combined.html")
    print("   - tests/dual_axis_profit.html")
    
    return combined_fig1, combined_fig2

def main():
    """主函数"""
    try:
        # 设置客户端
        client = setup_client()
        
        # 股票列表
        symbols = ['NVDA', 'TSLA', 'AAPL', 'MSFT']
        
        print("🚀 开始生成双轴可视化图表...")
        
        # 获取数据
        data = get_stock_performance_batch(client, symbols, limit=8)
        
        if not data:
            print("❌ 没有获取到任何数据")
            return
        
        print(f"✅ 成功获取 {len(data)} 只股票的数据")
        
        # 生成双轴图表
        print("📈 开始生成双轴图表...")
        generate_dual_axis_charts(data)
        
        print("\n🎉 双轴可视化完成！")
        
    except Exception as e:
        print(f"❌ 运行出错: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()