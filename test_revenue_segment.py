#!/usr/bin/env python3
"""
Test script for the new revenue_by_segment function
"""

import os
import sys
from dotenv import load_dotenv

# Add fmpxx to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fmpxx import FMPClient

# Load environment variables
load_dotenv()

def test_revenue_by_segment():
    """Test the revenue_by_segment function"""
    api_key = os.getenv('FMP_KEY')
    if not api_key:
        print("Please set FMP_KEY environment variable")
        return
    
    client = FMPClient(api_key, output_format='pandas')
    
    # Test with Apple (AAPL) - known to have segment data
    symbol = 'AAPL'
    
    print("Testing revenue_by_segment function...")
    print(f"Symbol: {symbol}")
    
    try:
        # Test geographic segments
        print("\n1. Testing geographic segments:")
        geo_df = client.financials.revenue_by_segment(symbol, structure='geographic', limit=5)
        print(f"Geographic segments shape: {geo_df.shape}")
        print(f"Columns: {list(geo_df.columns)}")
        if not geo_df.empty:
            print("First few rows:")
            print(geo_df.head())
        
        # Test product segments
        print("\n2. Testing product segments:")
        product_df = client.financials.revenue_by_segment(symbol, structure='product', limit=5)
        print(f"Product segments shape: {product_df.shape}")
        print(f"Columns: {list(product_df.columns)}")
        if not product_df.empty:
            print("First few rows:")
            print(product_df.head())
            
        # Test invalid structure parameter
        print("\n3. Testing invalid structure parameter:")
        try:
            invalid_df = client.financials.revenue_by_segment(symbol, structure='invalid')
        except ValueError as e:
            print(f"Expected error caught: {e}")
            
    except Exception as e:
        print(f"Error during testing: {e}")

if __name__ == "__main__":
    test_revenue_by_segment()