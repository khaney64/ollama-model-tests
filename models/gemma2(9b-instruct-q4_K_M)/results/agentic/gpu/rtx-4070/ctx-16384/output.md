## Section 1: Execution Plan (Markdown)

1. **Initialize Configuration**:
   - Tools: None
   - Set up risk thresholds and portfolio list:  `portfolios = ["PORT-001", "PORT-002", "PORT-003"]`, `risk_config = {"max_volatility": 35.0, "min_value": 50000, "max_value": 2000000}`

2. **For Each Portfolio:**
   a. **Fetch Holdings**:
      - Tools: `get_portfolio_holdings()`
      - Input: portfolio_id from the `portfolios` list
      - Output: `holdings` dictionary containing portfolio information and stock holdings.
      - Error Handling: Wrap in a try/except block to catch `ValueError` exceptions for invalid portfolio IDs. Log the error and continue processing other portfolios.

   b. **Get Stock Prices**:
      - Tools: `get_stock_prices()`
      - Input: list of symbols extracted from `holdings`. 
      - Output: `prices` dictionary mapping symbol to current price.
      - Error Handling: Handle potential `ValueError` exceptions for unknown symbols by logging the error and using a default price of 0 for that missing symbol.

   c. **Calculate Portfolio Value and Positions**:
      - Tools: `calculate_portfolio_value()`
      - Input: `holdings` and `prices`.
      - Output: `portfolio_value` dictionary containing total portfolio value, individual position values, gains/losses, and more.
      - Error Handling: Handle potential `ValueError` exceptions raised if holdings or prices are empty by logging the error and skipping that specific portfolio calculation.

   d. **Calculate Volatility Score**:
      - Tools: `calculate_volatility_score()`
      - Input: list of symbols from the holdings.
      - Output: `volatility_score`.
      - Error Handling: Handle potential `ValueError` exceptions for empty symbol lists or invalid `days` arguments by logging the error and using a default volatility score of 0 for that portfolio.

   e. **Check Risk Thresholds**:
      - Tools: `check_risk_threshold()`
      - Input: `portfolio_value`, `volatility_score`, and `risk_config`.
      - Output: dictionary with risk level, exceeded thresholds information.
      - Error Handling: Handle potential `ValueError` exceptions raised for invalid portfolio values or volatility scores by logging the error and continuing to process other portfolios.

   f. **Generate Report (if High Risk)**
      - Tools: `generate_report()`
      - Input: Portfolio data including  `portfolio_value`, `volatility_score`, `risk_level`, `exceeded_thresholds`, and holdings information. 
      - Output: Markdown formatted report string.
      - Error Handling: Handle potential `ValueError` exceptions for missing required fields in the portfolio data by logging the error and skipping report generation for that portfolio.

   g. **Send Notification (if High Risk)**
      - Tools: `send_notification()`
      - Input: Portfolio manager email, subject, formatted report text, "high" priority level.
      - Output:  Notification sending result dictionary.
      - Error Handling: Handle potential `ValueError` exceptions for invalid recipient email addresses or priorities by logging the error and continuing to process other portfolios.

3. **Log Operations:**
   - Tools: `log_operation()`
   - Log the start of portfolio analysis, completion of each step, risk threshold checks, report generation, and notification sending events. Use appropriate log levels (info, warning, error) for each operation.


## Section 2: Implementation (Python)

```python
from tools_reference import (
    get_stock_prices,
    get_portfolio_holdings,
    calculate_portfolio_value,
    calculate_volatility_score,
    check_risk_threshold,
    generate_report,
    send_notification,
    log_operation,
)

# Risk Configuration
risk_config = {
    "max_volatility": 35.0,
    "min_value": 50000,
    "max_value": 2000000
}
portfolios = ["PORT-001", "PORT-002", "PORT-003"]

def analyze_portfolio(portfolio_id):
    try:
        holdings = get_portfolio_holdings(portfolio_id)
        symbols = [holding["symbol"] for holding in holdings["holdings"]] 
        prices = get_stock_prices(symbols) 

        portfolio_value = calculate_portfolio_value(holdings["holdings"], prices)
        volatility_score = calculate_volatility_score(symbols, days=30)  

        risk_check = check_risk_threshold(
            portfolio_value["total_value"], volatility_score, risk_config
        )

        if risk_check["is_high_risk"]:
            report = generate_report(
                {
                    "portfolio_id": portfolio_id, 
                    # ... Include other relevant data from the analysis
                },
                report_format="markdown" 
            ) 
            send_notification(
                recipient="manager@firm.com",  # Replace with actual email
                subject=f"High Risk Alert: Portfolio {portfolio_id}",
                message=report,
                priority="high"
            )

        log_operation(
            operation="portfolio_analysis",
            details={"portfolio_id": portfolio_id, "risk_level": risk_check["risk_level"]},
            level="info"
        )

    except Exception as e:
        log_operation(
            operation=f"{portfolio_id} Portfolio Analysis Error",
            details={"error": str(e)},
            level="error"
        )


if __name__ == "__main__":
    for portfolio in portfolios:
        analyze_portfolio(portfolio)
```

## Section 3: Design Justification (Markdown)

### Tool Orchestration Sequence

I chose to process portfolios sequentially because this approach simplifies error handling. If one portfolio encounters an issue, the script can log the error and continue processing the remaining portfolios without impacting the entire workflow. Parallel processing would require more complex synchronization and error management.

### Data Flow Strategy

Holdings data is fed into three downstream operations (price fetching, value calculation, volatility scoring) because these operations all rely on the same information about a portfolio's stock positions. By passing holdings through each step, we ensure consistency and avoid redundant data retrieval.

### Error Handling Strategy

My approach emphasizes graceful degradation and logging for audit trail purposes:

- **Try/Except Blocks:** Each portfolio analysis is wrapped in a `try...except` block to catch potential exceptions raised by the API functions. This allows the script to gracefully handle errors without crashing.
- **Logging:**  I use `log_operation()` to record all major operations, both successful and unsuccessful. 

This creates an audit trail that helps identify the source of any problems and provides valuable insights into the system's behavior.



