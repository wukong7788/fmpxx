#!/usr/bin/env python3
"""
Simplified test script using agno's PythonTools for financial visualization.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add project root to path
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, project_root)

from agno.agent import Agent
from agno.tools.python import PythonTools


def test_visualization():
    """Test agno PythonTools for financial visualization using Gemini."""
    try:
        from agno.models.google import Gemini
        
        # Create agent with Python tools and Gemini
        python_agent = Agent(
            model=Gemini(id="gemini-2.0-flash-exp"),
            tools=[PythonTools(base_dir=Path("tmp/python"))], 
            show_tool_calls=True
        )
        
        print("🤖 Testing agno PythonTools with Gemini for AAPL visualization...")
        
        query = """
        Create a comprehensive financial visualization script for Apple Inc. (AAPL) stock performance.
        
        Requirements:
        1. Fetch 8 quarters of financial data including revenue, EPS, gross margin, operating margin, and free cash flow margin
        2. Create bar charts for revenue trends
        3. Create line charts for EPS growth
        4. Create multi-line charts for profitability margins
        5. Use professional styling with proper labels and titles
        6. Save plots as PNG files with high DPI
        7. Include summary statistics
        
        Use the fmpxx library to fetch data. Make it production-ready.
        """
        
        response = python_agent.print_response(query)
        return response
        
    except Exception as e:
        print(f"❌ Error during visualization: {e}")
        return None


if __name__ == "__main__":
    load_dotenv()
    
    # Check if required API keys are set
    api_key = os.getenv("FMP_KEY")
    gemini_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        print("Error: FMP_KEY environment variable is required")
        sys.exit(1)
    
    if not gemini_key:
        print("Warning: GEMINI_API_KEY not set, but continuing with PythonTools test")
    
    test_visualization()