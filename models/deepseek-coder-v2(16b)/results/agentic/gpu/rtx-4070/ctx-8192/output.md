 # Execution Plan

## 1. Initialize Configuration
- **Tools**: None
- **Set up risk thresholds** and portfolio list.
- **Configuration Data**:
  ```python
  risk_config = {
      "max_volatility": 35.0,
      "min_value": 50000,
      "max_value": 2000000
  }
  portfolios = ["PORT-001", "PORT-002", "PORT-003"]
  ```

## 2. For Each Portfolio:

### a. Fetch Holdings
- **Tool**: `get_portfolio_holdings()`
- **Input**: `portfolio_id`
- **Output**: `holdings` (needed for steps b, c, e)
- **Try/Except Block**: Handle exceptions if portfolio ID is invalid or not found.
  ```python
  try:
      holdings = get_portfolio_holdings(portfolio_id)
  except ValueError as e:
      log_operation("fetch_holdings", {"error": str(e)}, level="error")
      continue
  ```

### b. Get Stock Prices
- **Tool**: `get_stock_prices()`
- **Input**: List of symbols from `holdings`
- **Output**: `current_prices` (needed for step c)
- **Try/Except Block**: Handle exceptions if the list is empty or unknown symbols are encountered.
  ```python
  stock_symbols = [holding["symbol"] for holding in holdings["holdings"]]
  try:
      current_prices = get_stock_prices(stock_symbols)
  except ValueError as e:
      log_operation("fetch_stock_prices", {"error": str(e)}, level="error")
      continue
  ```

### c. Calculate Portfolio Value and Position Details
- **Tool**: `calculate_portfolio_value()`
- **Input**: `holdings` and `current_prices`
- **Output**: `portfolio_data` (needed for step d)
- **Try/Except Block**: Handle exceptions if the lists are empty or prices are missing.
  ```python
  try:
      portfolio_data = calculate_portfolio_value(holdings["holdings"], current_prices)
  except ValueError as e:
      log_operation("calculate_portfolio_value", {"error": str(e)}, level="error")
      continue
  ```

### d. Calculate Volatility Score
- **Tool**: `calculate_volatility_score()`
- **Input**: List of symbols from `holdings` and days (default: 30)
- **Output**: `volatility_score` (needed for step e)
- **Try/Except Block**: Handle exceptions if the list is empty or days are invalid.
  ```python
  try:
      volatility_score = calculate_volatility_score(stock_symbols, days=30)
  except ValueError as e:
      log_operation("calculate_volatility_score", {"error": str(e)}, level="error")
      continue
  ```

### e. Check Risk Threshold
- **Tool**: `check_risk_threshold()`
- **Input**: `portfolio_data["total_value"]`, `volatility_score`, and `risk_config`
- **Output**: `risk_check_result` (needed for step f)
- **Try/Except Block**: Handle exceptions if portfolio value or volatility score is negative.
  ```python
  try:
      risk_check_result = check_risk_threshold(portfolio_data["total_value"], volatility_score, risk_config)
  except ValueError as e:
      log_operation("check_risk_threshold", {"error": str(e)}, level="error")
      continue
  ```

### f. Generate and Send Report
- **Tool**: `generate_report()` and `send_notification()`
- **Input**: `portfolio_data` and risk check result, recipient email, priority "high"
- **Output**: `report` and `notification_result`
- **Try/Except Block**: Handle exceptions if required fields are missing or notification fails.
  ```python
  try:
      report = generate_report(portfolio_data)
      notification_result = send_notification("manager@firm.com", "High Risk Alert: Portfolio PORT-001", report, priority="high")
  except ValueError as e:
      log_operation("generate_and_send_report", {"error": str(e)}, level="error")
      continue
  ```

## 3. Error Handling Strategy
- **Wrap Each Portfolio in Try/Except**: If any step fails, the script continues to the next portfolio without crashing. Errors are logged and handled gracefully.
- **Log Errors and Continue**: Ensure that errors encountered during operations (e.g., invalid portfolio ID, missing prices) are captured and processed appropriately to avoid halting execution.

# Implementation

```python
from tools_reference import (
    get_stock_prices,
    get_portfolio_holdings,
    calculate_portfolio_value,
    calculate_volatility_score,
    check_risk_threshold,
    generate_report,
    send_notification,
    log_operation
)

def analyze_portfolios():
    risk_config = {
        "max_volatility": 35.0,
        "min_value": 50000,
        "max_value": 2000000
    }
    portfolios = ["PORT-001", "PORT-002", "PORT-003"]
    
    for portfolio_id in portfolios:
        try:
            # Step a: Fetch Holdings
            holdings = get_portfolio_holdings(portfolio_id)
            
            # Step b: Get Stock Prices
            stock_symbols = [holding["symbol"] for holding in holdings["holdings"]]
            current_prices = get_stock_prices(stock_symbols)
            
            # Step c: Calculate Portfolio Value and Position Details
            portfolio_data = calculate_portfolio_value(holdings["holdings"], current_prices)
            
            # Step d: Calculate Volatility Score
            volatility_score = calculate_volatility_score(stock_symbols, days=30)
            
            # Step e: Check Risk Threshold
            risk_check_result = check_risk_threshold(portfolio_data["total_value"], volatility_score, risk_config)
            
            # Step f: Generate and Send Report
            if risk_check_result["is_high_risk"]:
                report = generate_report(portfolio_data)
                notification_result = send_notification("manager@firm.com", "High Risk Alert: Portfolio PORT-001", report, priority="high")
        except ValueError as e:
            log_operation("analyze_portfolios", {"error": str(e)}, level="error")
            continue

if __name__ == "__main__":
    analyze_portfolios()
```

# Design Justification

## Tool Orchestration Sequence
I chose to process portfolios sequentially rather than in parallel because:
- Sequential processing is simpler and easier to manage with a fixed set of tools.
- It ensures that each portfolio's data is processed step by step, maintaining clarity in the workflow.

## Data Flow Strategy
Holdings data feeds into three downstream operations (price fetching, value calculation, volatility scoring) because:
- Accurate pricing information is crucial for calculating accurate position values and gains/losses.
- Volatility scores provide critical insights into risk levels that influence portfolio management decisions.

## Error Handling Strategy Rationale
The try/except block strategy ensures that any error encountered during the execution of a specific step does not halt the entire script but instead logs the error and moves to the next step, maintaining the integrity of data processing across all portfolios:
- **Graceful Degradation**: The system continues to process other portfolios even if one fails.
- **Debugging Aid**: Detailed log entries help in diagnosing issues encountered during runtime without affecting the overall workflow.

## Trade-offs Considered
While parallel processing could potentially increase speed, it introduces complexities such as thread safety and potential for overlapping errors that are difficult to debug. Sequential processing simplifies error handling and ensures a clear path of data transformation from input to output:
- **Complexity**: Parallel processing adds complexity due to the need for synchronization mechanisms and managing multiple threads.
- **Resource Utilization**: Sequential processing allows better control over system resources as it does not require concurrent execution, thus avoiding potential issues with resource contention.