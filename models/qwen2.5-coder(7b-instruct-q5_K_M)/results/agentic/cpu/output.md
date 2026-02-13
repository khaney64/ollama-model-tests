## Execution Plan (Markdown)

### Step-by-Step Execution Plan

1. **Initialize Configuration**
   - Tools: None
   - Set up risk thresholds and portfolio list
     ```python
     risk_config = {
         "max_volatility": 35.0,
         "min_value": 50000,
         "max_value": 2000000
     }
     portfolios = ["PORT-001", "PORT-002", "PORT-003"]
     ```

2. **For Each Portfolio:**
   - a. **Fetch Holdings**
     - Tool: get_portfolio_holdings()
     - Input: portfolio_id
     - Output: holdings data (needed for steps b, c, e)
       ```python
       try:
           holdings = get_portfolio_holdings(portfolio_id)
       except ValueError as e:
           log_operation("portfolio_fetch", {"portfolio_id": portfolio_id, "error": str(e)}, level="error")
           continue  # Skip to next portfolio on error
       ```

   - b. **Get Stock Prices**
     - Tool: get_stock_prices()
     - Input: symbols extracted from holdings
     - Output: current prices (needed for step c)
       ```python
       symbols = [holding["symbol"] for holding in holdings["holdings"]]
       try:
           prices = get_stock_prices(symbols)
       except ValueError as e:
           log_operation("price_fetch", {"portfolio_id": portfolio_id, "error": str(e)}, level="error")
           continue  # Skip to next portfolio on error
       ```

   - c. **Calculate Portfolio Value and Positions**
     - Tool: calculate_portfolio_value()
     - Input: holdings, prices
     - Output: portfolio value, position details (needed for steps d, e)
       ```python
       try:
           value_data = calculate_portfolio_value(holdings["holdings"], prices)
       except ValueError as e:
           log_operation("value_calc", {"portfolio_id": portfolio_id, "error": str(e)}, level="error")
           continue  # Skip to next portfolio on error
       ```

   - d. **Calculate Volatility Score**
     - Tool: calculate_volatility_score()
     - Input: symbols, days (30)
     - Output: volatility score (needed for step e)
       ```python
       try:
           volatility = calculate_volatility_score(symbols, 30)
       except ValueError as e:
           log_operation("volatility_calc", {"portfolio_id": portfolio_id, "error": str(e)}, level="error")
           continue  # Skip to next portfolio on error
       ```

   - e. **Check Risk Thresholds**
     - Tool: check_risk_threshold()
     - Input: portfolio_value, volatility_score, risk_config
     - Output: risk status (needed for step f)
       ```python
       try:
           risk_check = check_risk_threshold(value_data["total_value"], volatility, risk_config)
       except ValueError as e:
           log_operation("risk_check", {"portfolio_id": portfolio_id, "error": str(e)}, level="error")
           continue  # Skip to next portfolio on error

       if risk_check["is_high_risk"]:
           # f. Generate Report
           - Tool: generate_report()
             - Input: portfolio_data, report_format ("markdown")
             - Output: formatted report (needed for step g)
               ```python
               try:
                   report = generate_report({
                       "portfolio_id": portfolio_id,
                       "client_name": holdings["client_name"],
                       "total_value": value_data["total_value"],
                       "volatility_score": volatility,
                       "risk_level": risk_check["risk_level"],
                       "exceeded_thresholds": risk_check["exceeded_thresholds"],
                       "positions": value_data["positions"]
                   }, report_format="markdown")
               except ValueError as e:
                   log_operation("report_gen", {"portfolio_id": portfolio_id, "error": str(e)}, level="error")
                   continue  # Skip to next portfolio on error
           
           # g. Send Notification
           - Tool: send_notification()
             - Input: recipient (manager_email), subject, message, priority ("high")
             - Output: notification result
               ```python
               try:
                   result = send_notification(
                       holdings["manager_email"],
                       f"High Risk Alert: Portfolio {portfolio_id}",
                       report,
                       priority="high"
                   )
                   log_operation("notification_sent", {"portfolio_id": portfolio_id, "message_id": result["message_id"]}, level="info")
               except ValueError as e:
                   log_operation("notification_err", {"portfolio_id": portfolio_id, "error": str(e)}, level="error")
   ```

3. **Error Handling Strategy**
   - Wrap each portfolio processing in `try/except` blocks to handle errors gracefully.
   - Log errors using `log_operation()` for audit trail.

## Implementation (Python)

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
    """Main orchestration function."""
    risk_config = {
        "max_volatility": 35.0,
        "min_value": 50000,
        "max_value": 2000000
    }
    portfolios = ["PORT-001", "PORT-002", "PORT-003"]
    
    log_operation("portfolio_analysis_start", {}, level="info")
    
    for portfolio_id in portfolios:
        try:
            # a. Fetch Holdings
            holdings = get_portfolio_holdings(portfolio_id)
            
            # b. Get Stock Prices
            symbols = [holding["symbol"] for holding in holdings["holdings"]]
            prices = get_stock_prices(symbols)
            
            # c. Calculate Portfolio Value and Positions
            value_data = calculate_portfolio_value(holdings["holdings"], prices)
            
            # d. Calculate Volatility Score
            volatility = calculate_volatility_score(symbols, 30)
            
            # e. Check Risk Thresholds
            risk_check = check_risk_threshold(value_data["total_value"], volatility, risk_config)
            
            if risk_check["is_high_risk"]:
                # f. Generate Report
                report = generate_report({
                    "portfolio_id": portfolio_id,
                    "client_name": holdings["client_name"],
                    "total_value": value_data["total_value"],
                    "volatility_score": volatility,
                    "risk_level": risk_check["risk_level"],
                    "exceeded_thresholds": risk_check["exceeded_thresholds"],
                    "positions": value_data["positions"]
                }, report_format="markdown")
                
                # g. Send Notification
                result = send_notification(
                    holdings["manager_email"],
                    f"High Risk Alert: Portfolio {portfolio_id}",
                    report,
                    priority="high"
                )
                log_operation("notification_sent", {"portfolio_id": portfolio_id, "message_id": result["message_id"]}, level="info")
            
        except Exception as e:
            log_operation("analysis_err", {"portfolio_id": portfolio_id, "error": str(e)}, level="error")
    
    log_operation("portfolio_analysis_complete", {}, level="info")

if __name__ == "__main__":
    analyze_portfolios()
```

## Design Justification (Markdown)

### Tool Orchestration Sequence

1. **Initialize Configuration**: Set up risk thresholds and portfolio list.
2. **For Each Portfolio**:
   - Fetch holdings to get basic details about the portfolio.
   - Get stock prices for all holdings to calculate current value.
   - Calculate total portfolio value and individual position values.
   - Determine volatility score based on historical data.
   - Check if the portfolio exceeds risk thresholds.
   - Generate a detailed report in markdown format if high-risk.
   - Send a notification with high priority to the portfolio manager.

### Data Flow Strategy

- **Input:** Portfolio ID
- **Process:** 
  - Fetch holdings, calculate values, volatility, and check risk.
  - If high-risk, generate report and send notification.
- **Output:** 
  - Detailed report if high-risk.
  - Notification sent to portfolio manager.

### Error Handling Strategy

- Wrap each step in `try/except` blocks to catch and log errors.
- Continue processing remaining portfolios even if one fails.
- Log all operations for audit trail.

### Trade-offs Considered

- **Sequential Processing**: Ensures that each step is completed before moving on, which can be time-consuming but ensures accuracy and correctness.
- **Error Graceful Handling**: Ensures the system can continue running even if a single portfolio fails, maintaining robustness.
- **Audit Trail**: Maintains a record of all operations for debugging and compliance purposes.

This design ensures that the script is well-structured, maintainable, and adheres to the requirements specified in the task.