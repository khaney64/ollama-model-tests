## Execution Plan (Markdown)

### Step-by-Step Execution Plan

1. **Initialize Configuration**
   - Tools: None
   - Set up risk thresholds and portfolio list:
     ```python
     risk_config = {
         "max_volatility": 35.0,
         "min_value": 50000,
         "max_value": 2000000
     }
     portfolios = ["PORT-001", "PORT-002", "PORT-003"]
     ```

2. **For Each Portfolio:**
   - Tools: get_portfolio_holdings(), get_stock_prices(), calculate_portfolio_value(), calculate_volatility_score(), check_risk_threshold()
   - Data dependencies between steps:
     - get_stock_prices() depends on get_portfolio_holdings() to fetch symbols
     - calculate_portfolio_value() depends on get_portfolio_holdings() and get_stock_prices()
     - calculate_volatility_score() depends on the symbols from portfolio holdings
     - check_risk_threshold() depends on calculate_portfolio_value() and calculate_volatility_score()

   a. **Fetch Holdings**
      - Tool: get_portfolio_holdings()
      - Input: portfolio_id (e.g., "PORT-001")
      - Output: holdings data (needed for steps b, c)

   b. **Get Stock Prices**
      - Tool: get_stock_prices()
      - Input: symbols extracted from holdings
      - Output: current prices (needed for step c)

   c. **Calculate Portfolio Value**
      - Tool: calculate_portfolio_value()
      - Input: holdings data and current stock prices
      - Output: portfolio value, position details (needed for step d)

   d. **Calculate Volatility Score**
      - Tool: calculate_volatility_score()
      - Input: symbols from holdings and 30-day period
      - Output: volatility score (needed for step e)

   e. **Check Risk Thresholds**
      - Tool: check_risk_threshold()
      - Input: portfolio value, volatility score, risk_config
      - Output: is_high_risk, exceeded_thresholds, risk_level

   f. **Generate Report and Send Notification**
      - Tools: generate_report(), send_notification()
      - Input: portfolio data (from steps a-e), report_format="markdown", recipient=manager_email from portfolio data
      - Output: generated report string and notification status

3. **Error Handling Strategy**
   - Wrap each portfolio processing in try/except blocks to catch and log errors:
     ```python
     try:
         # Steps a-e for one portfolio
         pass
     except ValueError as e:
         log_operation("error", {"portfolio_id": portfolio_id, "error": str(e)}, level="error")
         print(f"Error processing {portfolio_id}: {e}")
         continue
     ```
   - Continue processing remaining portfolios if one fails.

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

    for portfolio_id in portfolios:
        try:
            # Step a: Fetch Holdings
            portfolio = get_portfolio_holdings(portfolio_id)
            symbols = [item['symbol'] for item in portfolio['holdings']]
            log_operation("portfolio_analysis", {"portfolio_id": portfolio_id, "operation": "fetch_holdings"})

            # Step b: Get Stock Prices
            prices = get_stock_prices(symbols)
            log_operation("portfolio_analysis", {"portfolio_id": portfolio_id, "operation": "get_stock_prices", "symbols": symbols})

            # Step c: Calculate Portfolio Value
            value_data = calculate_portfolio_value(portfolio['holdings'], prices)
            total_value = value_data['total_value']
            log_operation("portfolio_analysis", {"portfolio_id": portfolio_id, "operation": "calculate_portfolio_value", "total_value": total_value})

            # Step d: Calculate Volatility Score
            volatility_score = calculate_volatility_score(symbols)
            log_operation("portfolio_analysis", {"portfolio_id": portfolio_id, "operation": "calculate_volatility_score", "volatility_score": volatility_score})

            # Step e: Check Risk Thresholds
            risk_check = check_risk_threshold(total_value, volatility_score, risk_config)
            is_high_risk = risk_check['is_high_risk']
            log_operation("portfolio_analysis", {"portfolio_id": portfolio_id, "operation": "check_risk_threshold", "risk_level": risk_check['risk_level']})

            # Step f: Generate Report and Send Notification
            if is_high_risk:
                report_text = generate_report({
                    **portfolio,
                    **value_data,
                    **risk_check
                }, report_format="markdown")
                result = send_notification(
                    portfolio['manager_email'],
                    "High Risk Alert: Portfolio {}".format(portfolio_id),
                    report_text,
                    priority="high"
                )
                log_operation("portfolio_analysis", {"portfolio_id": portfolio_id, "operation": "send_notification", "sent": result["sent"]})

        except ValueError as e:
            log_operation("error", {"portfolio_id": portfolio_id, "error": str(e)}, level="error")
            print(f"Error processing {portfolio_id}: {e}")

if __name__ == "__main__":
    analyze_portfolios()
```

## Design Justification (Markdown)

### Tool Orchestration Sequence
I chose to process portfolios sequentially rather than in parallel because:
- Sequential processing ensures that dependencies are met before moving on to the next step.
- It simplifies error handling and logging, as issues can be isolated and addressed individually.

### Data Flow Strategy
Holdings data feeds into three downstream operations (price fetching, value calculation, volatility scoring) because:
- Each operation requires a specific set of inputs from the previous steps.
- This modular approach allows for easier maintenance and testing of individual components.

### Error Handling Strategy Rationale
- Wrapping each portfolio processing in try/except blocks ensures that errors do not propagate to other portfolios.
- Proper logging captures all relevant information, facilitating troubleshooting and audit trail maintenance.

### Trade-offs Considered
- Sequential processing avoids potential concurrency issues but can be slower than parallel execution.
- The trade-off is between simplicity of implementation and performance efficiency.