#!/usr/bin/env python3
"""
批量股票业绩分析和可视化工具

功能：
1. 批量获取股票业绩数据并保存CSV
2. 使用Plotly创建对比图表
3. 支持营收、营业利润、质量指标等可视化
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
                csv_path = f'tests/test_data/performance_{symbol}.csv'
                df.to_csv(csv_path, index=False)
                print(f"✅ {symbol} 数据已保存到 {csv_path}")
            else:
                print(f"❌ 无法获取 {symbol} 的数据")
        except Exception as e:
            print(f"❌ 获取 {symbol} 数据时出错: {str(e)}")
    
    return results

def plot_gross_margin_ratio(data_dict):
    """
    绘制毛利率对比图
    
    Args:
        data_dict: 股票代码到DataFrame的映射
    """
    if not data_dict:
        print("没有数据可供绘图")
        return
    
    fig = go.Figure()
    
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
    
    for i, (symbol, df) in enumerate(data_dict.items()):
        color = colors[i % len(colors)]
        df = df.sort_values('period_date')
        
        # 毛利率对比
        fig.add_trace(
            go.Scatter(
                x=df['period_date'], 
                y=df['grossProfitRatio']*100,
                name=f'{symbol}',
                line=dict(color=color, width=2),
                mode='lines+markers'
            )
        )
    
    fig.update_layout(
        title='毛利率对比分析 (%)',
        height=400,
        showlegend=True,
        template='plotly_white',
        xaxis_title="报告期",
        yaxis_title="毛利率 (%)"
    )
    
    return fig

def plot_operating_margin_ratio(data_dict):
    """
    绘制营业利润率对比图
    
    Args:
        data_dict: 股票代码到DataFrame的映射
    """
    if not data_dict:
        print("没有数据可供绘图")
        return
    
    fig = go.Figure()
    
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
    
    for i, (symbol, df) in enumerate(data_dict.items()):
        color = colors[i % len(colors)]
        df = df.sort_values('period_date')
        
        # 营业利润率对比
        fig.add_trace(
            go.Scatter(
                x=df['period_date'], 
                y=df['operatingIncomeRatio']*100,
                name=f'{symbol}',
                line=dict(color=color, width=2),
                mode='lines+markers'
            )
        )
    
    fig.update_layout(
        title='营业利润率对比分析 (%)',
        height=400,
        showlegend=True,
        template='plotly_white',
        xaxis_title="报告期",
        yaxis_title="营业利润率 (%)"
    )
    
    return fig

def plot_free_cashflow_margin(data_dict):
    """
    绘制自由现金流利润率对比图
    
    Args:
        data_dict: 股票代码到DataFrame的映射
    """
    if not data_dict:
        print("没有数据可供绘图")
        return
    
    fig = go.Figure()
    
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
    
    for i, (symbol, df) in enumerate(data_dict.items()):
        color = colors[i % len(colors)]
        df = df.sort_values('period_date')
        
        # 自由现金流利润率对比
        fig.add_trace(
            go.Scatter(
                x=df['period_date'], 
                y=df['freeCashFlowMargin']*100,
                name=f'{symbol}',
                line=dict(color=color, width=2),
                mode='lines+markers'
            )
        )
    
    fig.update_layout(
        title='自由现金流利润率对比分析 (%)',
        height=400,
        showlegend=True,
        template='plotly_white',
        xaxis_title="报告期",
        yaxis_title="自由现金流利润率 (%)"
    )
    
    return fig

def plot_debt_to_asset_ratio(data_dict):
    """
    绘制资产负债率对比图
    
    Args:
        data_dict: 股票代码到DataFrame的映射
    """
    if not data_dict:
        print("没有数据可供绘图")
        return
    
    fig = go.Figure()
    
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
    
    for i, (symbol, df) in enumerate(data_dict.items()):
        color = colors[i % len(colors)]
        df = df.sort_values('period_date')
        
        # 资产负债率对比
        fig.add_trace(
            go.Scatter(
                x=df['period_date'], 
                y=df['debtToAssetRatio']*100,
                name=f'{symbol}',
                line=dict(color=color, width=2),
                mode='lines+markers'
            )
        )
    
    fig.update_layout(
        title='资产负债率对比分析 (%)',
        height=400,
        showlegend=True,
        template='plotly_white',
        xaxis_title="报告期",
        yaxis_title="资产负债率 (%)"
    )
    
    return fig

def plot_comprehensive_analysis(data_dict):
    """
    绘制营收和利润对比图
    
    Args:
        data_dict: 股票代码到DataFrame的映射
    """
    if not data_dict:
        print("没有数据可供绘图")
        return
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            '营收对比 (十亿美元)', 
            '营收增长率对比 (%)',
            '营业利润对比 (十亿美元)', 
            '营业利润增长率对比 (%)'
        ),
        vertical_spacing=0.15,
        horizontal_spacing=0.1
    )
    
    colors = px.colors.qualitative.Set1
    
    for i, (symbol, df) in enumerate(data_dict.items()):
        color = colors[i % len(colors)]
        
        # 营收对比
        fig.add_trace(
            go.Scatter(
                x=df['period_date'], 
                y=df['revenue']/1e9,
                name=f'{symbol} 营收',
                line=dict(color=color, width=2),
                mode='lines+markers',
            ),
            row=1, col=1
        )
        
        # 营收增长率对比
        fig.add_trace(
            go.Scatter(
                x=df['period_date'], 
                y=df['revenue_growth_rate']*100,
                name=f'{symbol} 营收增长率',
                line=dict(color=color, width=2, dash='dash'),
                mode='lines+markers',
            ),
            row=1, col=2
        )
        
        # 营业利润对比
        fig.add_trace(
            go.Scatter(
                x=df['period_date'], 
                y=df['operatingIncome']/1e9,
                name=f'{symbol} 营业利润',
                line=dict(color=color, width=2),
                mode='lines+markers',
            ),
            row=2, col=1
        )
        
        # 营业利润增长率对比
        fig.add_trace(
            go.Scatter(
                x=df['period_date'], 
                y=df['operatingIncome_growth_rate']*100,
                name=f'{symbol} 营业利润增长率',
                line=dict(color=color, width=2, dash='dash'),
                mode='lines+markers',
            ),
            row=2, col=2
        )
        
        # 毛利率
        fig.add_trace(
            go.Scatter(
                x=df['period_date'], 
                y=df['grossProfitRatio']*100,
                name=f'{symbol} 毛利率',
                line=dict(color=color, width=2),
                mode='lines+markers',
            ),
            row=3, col=1
        )
        
        # 营业利润率
        fig.add_trace(
            go.Scatter(
                x=df['period_date'], 
                y=df['operatingIncomeRatio']*100,
                name=f'{symbol} 营业利润率',
                line=dict(color=color, width=2, dash='dot'),
                mode='lines+markers',
            ),
            row=3, col=1
        )
        
        # 自由现金流利润率
        fig.add_trace(
            go.Scatter(
                x=df['period_date'], 
                y=df['freeCashFlowMargin']*100,
                name=f'{symbol} 自由现金流利润率',
                line=dict(color=color, width=2),
                mode='lines+markers',
            ),
            row=3, col=2
        )
        
        # 资产负债率
        fig.add_trace(
            go.Scatter(
                x=df['period_date'], 
                y=df['debtToAssetRatio']*100,
                name=f'{symbol} 资产负债率',
                line=dict(color=color, width=2, dash='dash'),
                mode='lines+markers',
            ),
            row=3, col=2
        )
    
    # 更新布局
    fig.update_layout(
        title='营收和利润对比分析',
        height=400,
        showlegend=True,
        template='plotly_white',
        hovermode='x unified'
    )
    
    # 更新坐标轴标签
    fig.update_yaxes(title_text="营收 (十亿美元)", row=1, col=1)
    fig.update_yaxes(title_text="营收增长率 (%)", row=1, col=2)
    fig.update_yaxes(title_text="营业利润 (十亿美元)", row=2, col=1)
    fig.update_yaxes(title_text="营业利润增长率 (%)", row=2, col=2)
    
    fig.update_xaxes(title_text="报告期", row=2, col=1)
    fig.update_xaxes(title_text="报告期", row=2, col=2)
    
    return fig

def generate_all_charts_html(data_dict):
    """
    生成包含所有图表的单一HTML文件
    
    Args:
        data_dict: 股票代码到DataFrame的映射
    """
    if not data_dict:
        print("没有数据可供绘图")
        return
    
    from plotly.subplots import make_subplots
    
    # 创建子图：6个独立的图表，2列3行
    fig = make_subplots(
        rows=4, cols=2,
        subplot_titles=(
            '营收对比 (十亿美元)', 
            '营收增长率对比 (%)',
            '营业利润对比 (十亿美元)', 
            '营业利润增长率对比 (%)',
            '毛利率对比 (%)',
            '营业利润率对比 (%)',
            '自由现金流利润率对比 (%)',
            '资产负债率对比 (%)'
        ),
        vertical_spacing=0.12,
        horizontal_spacing=0.1,
        specs=[
            [{"secondary_y": False}, {"secondary_y": False}],
            [{"secondary_y": False}, {"secondary_y": False}],
            [{"secondary_y": False}, {"secondary_y": False}],
            [{"secondary_y": False}, {"secondary_y": False}]
        ]
    )
    
    colors = px.colors.qualitative.Set1
    
    for i, (symbol, df) in enumerate(data_dict.items()):
        color = colors[i % len(colors)]
        df = df.sort_values('period_date')
        
        # 第1行：营收和营收增长率
        fig.add_trace(
            go.Scatter(
                x=df['period_date'], 
                y=df['revenue']/1e9,
                name=f'{symbol} 营收',
                line=dict(color=color, width=2),
                mode='lines+markers',
                legendgroup=f'group{i+1}'
            ),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=df['period_date'], 
                y=df['revenue_growth_rate']*100,
                name=f'{symbol} 营收增长率',
                line=dict(color=color, width=2),
                mode='lines+markers',
                legendgroup=f'group{i+1}'
            ),
            row=1, col=2
        )
        
        # 第2行：营业利润和营业利润增长率
        fig.add_trace(
            go.Scatter(
                x=df['period_date'], 
                y=df['operatingIncome']/1e9,
                name=f'{symbol} 营业利润',
                line=dict(color=color, width=2),
                mode='lines+markers',
                legendgroup=f'group{i+1}'
            ),
            row=2, col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=df['period_date'], 
                y=df['operatingIncome_growth_rate']*100,
                name=f'{symbol} 营业利润增长率',
                line=dict(color=color, width=2),
                mode='lines+markers',
                legendgroup=f'group{i+1}'
            ),
            row=2, col=2
        )
        
        # 第3行：毛利率和营业利润率
        fig.add_trace(
            go.Scatter(
                x=df['period_date'], 
                y=df['grossProfitRatio']*100,
                name=f'{symbol} 毛利率',
                line=dict(color=color, width=2),
                mode='lines+markers',
                legendgroup=f'group{i+1}'
            ),
            row=3, col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=df['period_date'], 
                y=df['operatingIncomeRatio']*100,
                name=f'{symbol} 营业利润率',
                line=dict(color=color, width=2),
                mode='lines+markers',
                legendgroup=f'group{i+1}'
            ),
            row=3, col=2
        )
        
        # 第4行：自由现金流利润率和资产负债率
        fig.add_trace(
            go.Scatter(
                x=df['period_date'], 
                y=df['freeCashFlowMargin']*100,
                name=f'{symbol} 自由现金流利润率',
                line=dict(color=color, width=2),
                mode='lines+markers',
                legendgroup=f'group{i+1}'
            ),
            row=4, col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=df['period_date'], 
                y=df['debtToAssetRatio']*100,
                name=f'{symbol} 资产负债率',
                line=dict(color=color, width=2),
                mode='lines+markers',
                legendgroup=f'group{i+1}'
            ),
            row=4, col=2
        )
    
    # 更新布局
    fig.update_layout(
        title='股票业绩综合分析报告',
        height=1600,
        showlegend=True,
        template='plotly_white',
        hovermode='x unified'
    )
    
    # 更新坐标轴标签
    fig.update_yaxes(title_text="营收 (十亿美元)", row=1, col=1)
    fig.update_yaxes(title_text="营收增长率 (%)", row=1, col=2)
    fig.update_yaxes(title_text="营业利润 (十亿美元)", row=2, col=1)
    fig.update_yaxes(title_text="营业利润增长率 (%)", row=2, col=2)
    fig.update_yaxes(title_text="毛利率 (%)", row=3, col=1)
    fig.update_yaxes(title_text="营业利润率 (%)", row=3, col=2)
    fig.update_yaxes(title_text="自由现金流利润率 (%)", row=4, col=1)
    fig.update_yaxes(title_text="资产负债率 (%)", row=4, col=2)
    
    fig.update_xaxes(title_text="报告期", row=4, col=1)
    fig.update_xaxes(title_text="报告期", row=4, col=2)
    
    # 保存图表
    fig.write_html('tests/test_data/all_charts_analysis.html')
    print("📊 所有图表已保存到 tests/test_data/all_charts_analysis.html")
    
    return fig

def main():
    """主函数"""
    try:
        # 设置客户端
        client = setup_client()
        
        # 股票列表
        symbols = ['NVDA', 'TSLA', 'AAPL', 'MSFT','AMZN', 'META','GOOGL']
        
        print("🚀 开始批量股票业绩分析...")
        
        # 获取数据
        data = get_stock_performance_batch(client, symbols, limit=8)
        
        if not data:
            print("❌ 没有获取到任何数据")
            return
        
        print(f"✅ 成功获取 {len(data)} 只股票的数据")
        
        # 生成图表
        print("📈 开始生成图表...")
        generate_all_charts_html(data)
        
        print("\n🎉 分析完成！")
        print("📁 生成的文件:")
        for symbol in symbols:
            if symbol in data:
                print(f"   - tests/test_data/performance_{symbol}.csv")
        print("   - tests/test_data/all_charts_analysis.html")
        
    except Exception as e:
        print(f"❌ 运行出错: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()