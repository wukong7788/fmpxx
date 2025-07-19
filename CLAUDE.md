# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**fmpxx** is a Python SDK for accessing Financial Modeling Prep (FMP) API, providing financial market data including stock quotes, company financials, and historical pricing data.

## Architecture

The codebase follows a modular design with these key components:

- **FMPClient**: Main entry point in `fmpxx/__init__.py:5` that provides access to categorized API modules
- **_BaseClient**: Base class in `fmpxx/base.py:5` handling HTTP requests, error handling, and response processing
- **Financials**: Company fundamental data (income statements, balance sheets, cash flow) in `fmpxx/financials.py:13`
- **Stocks**: Stock market data (historical prices, quotes, search) in `fmpxx/stocks.py:5`
- ~~AI Agent~~: Removed interactive simulator (was in `fmpxx/agent/interactive_agent.py`)

## Common Commands

### Development Setup
```bash
# Install uv package manager
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment and install dependencies
uv venv
uv install .

# Activate environment
source .venv/bin/activate
```

### Testing
```bash
# Run all tests
python tests/tests.py

# Run individual test modules
python tests/tests2.py

# Note: Tests require FMP_KEY environment variable
```


### Environment Setup
Create `.env` file with required variables:
```
FMP_KEY=your_fmp_api_key
```

## Key API Classes

### FMPClient
- **Location**: `fmpxx/__init__.py:5`
- **Usage**: `client = FMPClient(api_key, output_format='pandas')`
- **Properties**: 
  - `financials`: Access to company financial data
  - `stocks`: Access to stock market data

### Financials
- **Location**: `fmpxx/financials.py:13`
- **Key Methods**:
  - `get_financials(symbol, statement, limit=10, period='quarter')`
  - `get_merged_financials(symbol, limit=40, period='quarter')`

### Stocks
- **Location**: `fmpxx/stocks.py:5`
- **Key Methods**:
  - `historical_price_full(symbol, start=None, end=None, period=None)`
  - `quote(symbol)`
  - `search(query, limit=10)`
  - `stock_list()`

## Error Handling

The codebase uses custom exceptions in `fmpxx/exceptions.py`:
- `FMPAPIError`: Generic API errors
- `InvalidAPIKeyError`: Authentication failures
- `SymbolNotFoundError`: Missing stock symbols
- `RateLimitExceededError`: API rate limits
- `FMPConnectionError`: Network/timeout issues

## Response Formats

- **JSON**: Default format when `output_format='json'`
- **Pandas DataFrame**: When `output_format='pandas'` (recommended for analysis)
- Columns "link" and "finalLink" are automatically dropped in pandas mode

## Dependencies

Core dependencies are managed via `pyproject.toml`:
- `pandas>=2.2.3`
- `requests>=2.32.3`
- `python-dotenv>=1.0.1`
- `retry>=0.9.2`

Python requires >=3.11.11