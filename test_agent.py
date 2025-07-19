#!/usr/bin/env python3
"""
Test script for the Financial AI Agent.
This script demonstrates how to use the fin_ai_agent to query financial data.

Examples:
    # Query stock data
    python test_agent.py "帮我查一下苹果公司（AAPL）最近5天的日K线数据"
    
    # Query financial data
    python test_agent.py "特斯拉（TSLA）最新的年度资产负债表是什么？"
    
    # Interactive chat mode
    python test_agent.py --chat
"""

import os
import sys
import argparse
from dotenv import load_dotenv

# Add project root to path
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, project_root)

from fmpxx import create_agent


def main():
    """Main test function."""
    parser = argparse.ArgumentParser(description="Test Financial AI Agent")
    parser.add_argument("query", nargs="?", help="Question to ask the agent")
    parser.add_argument("--chat", action="store_true", help="Start interactive chat mode")
    parser.add_argument("--api-key", help="FMP API key (overrides environment)")
    parser.add_argument("--gemini-key", help="Gemini API key (overrides environment)")
    
    args = parser.parse_args()
    
    # Load environment variables
    load_dotenv()
    
    # Get API keys
    api_key = args.api_key or os.getenv("FMP_KEY")
    gemini_key = args.gemini_key or os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        print("Error: FMP API key is required. Set FMP_KEY environment variable or use --api-key")
        sys.exit(1)
    
    if not gemini_key:
        print("Error: Gemini API key is required. Set GEMINI_API_KEY environment variable or use --gemini-key")
        sys.exit(1)
    
    # Create agent
    print("🤖 Initializing Financial AI Agent...")
    agent = create_agent(api_key=api_key, gemini_api_key=gemini_key)
    
    if args.chat:
        # Interactive mode
        print("Starting interactive chat...")
        agent.chat()
    elif args.query:
        # Single query mode
        print(f"📝 Query: {args.query}")
        print("-" * 50)
        response = agent.query(args.query)
        print(response)
    else:
        # Demo mode
        print("🎯 Running demo queries...")
        
        demo_queries = [
            "帮我查一下苹果公司（AAPL）最近5天的日K线数据",
            "特斯拉（TSLA）最新的年度资产负债表是什么？",
            "微软（MSFT）最新的季度利润表数据",
            "谷歌（GOOGL）的实时股价是多少？",
            "搜索一下包含'半导体'的公司"
        ]
        
        for query in demo_queries:
            print(f"\n📝 Query: {query}")
            print("-" * 50)
            try:
                response = agent.query(query)
                print(response)
            except Exception as e:
                print(f"❌ Error: {e}")
            print("\n" + "=" * 70 + "\n")


if __name__ == "__main__":
    main()