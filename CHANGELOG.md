## Changelog

### 0.2.8
- Added interactive AI Agent simulator (`fmpxx/agent/interactive_agent.py`) to demonstrate natural language interaction with the library.
- Updated `README.md` with instructions for the AI Agent simulator.

### 0.2.7
- Refactored `financials.py`:
    - Consolidated specific financial statement methods (income, balance, cash flow, ratios, enterprise value, key metrics, growth metrics) into a single, more flexible `get_financials` function.
    - Optimized `get_financials` to leverage `_process_response` for consistent Pandas DataFrame conversion and column cleaning.
    - Updated `get_merged_financials` to use the new `get_financials` signature and incorporate robust data merging and cleaning logic.
- Renamed `company_fundamentals.py` to `financials.py` and updated all references.
- Updated `README.md` and `tests.py` to reflect the new API structure and usage.
- Enhanced Pandas display options in `tests.py` for better output readability.