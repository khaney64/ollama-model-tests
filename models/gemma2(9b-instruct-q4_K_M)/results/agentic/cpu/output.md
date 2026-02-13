## Section 1: Execution Plan

1. **Initialize Configuration**:
    - Tools: None
    - Define risk thresholds: `max_volatility = 35.0`, `min_value = 50000`, `max_value = 2000000`
    - Set portfolio list: `portfolios = ["PORT-001", "PORT-002", "PORT-003"]`

2. **Process Each Portfolio**: For each portfolio in the `portfolios` list
   a. **Fetch Holdings**:
     - Tool: `get_portfolio_holdings()`
     - Input: Portfolio ID (`portfolio_id`)
     - Output: `holdings` (dictionary with portfolio information and holdings)
   b. **Get Stock Prices**:
     - Tool: `get_stock_prices()`
     - Input: List of symbols from `holdings['holdings']`
     - Output: `current_prices` (dictionary mapping symbols to prices)
   c. **Calculate Portfolio Value & Metrics**:
     - Tool: `calculate_portfolio_value()`
     - Input: `holdings`, `current_prices`
     - Output: `portfolio_data` (dictionary with total value, position details, etc.)
     - Calculate volatility score using `calculate_volatility_score()`. 
     - Input: Symbols from `holdings['holdings']`
     - Output: `volatility_score`

   d. **Check Risk Thresholds**:
     - Tool: `check_risk_threshold()`
     - Input: `portfolio_data['total_value']`, `volatility_score`, risk thresholds dictionary
     - Output: `risk_check` (dictionary with risk level, exceeded thresholds)

   e. **Generate Report & Send Notification**: If `risk_check['is_high_risk']` is True:
     - Tool: `generate_report()`, `send_notification()`
     - Input: `portfolio_data`, `risk_check`
     - Output: report (markdown string), notification sent confirmation

3. **Log Operations**: 
    - Use `log_operation()` after each major step: fetching holdings, calculating metrics, risk check, report generation, notification sending

**Error Handling Strategy:**

*   Wrap each portfolio analysis in a `try...except` block to catch potential errors like invalid IDs or missing data.
*   Log the error details using `log_operation()` with "error" level. 
*   Print an informative message to the console indicating the error and which portfolio was affected.
*   Continue processing the remaining portfolios, avoiding program termination on a single error.



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
    log_operation
)

RISK_THRESHOLDS = {
    "max_volatility": 35.0,
    "min_value": 50000,
    "max_value": 2000000
}

portfolios = ["PORT-001", "PORT-002", "PORT-003"]


def analyze_portfolio(portfolio_id):
    try:
        holdings = get_portfolio_holdings(portfolio_id)
        symbols = [holding["symbol"] for holding in holdings["holdings"]]

        current_prices = get_stock_prices(symbols)
        portfolio_data = calculate_portfolio_value(holdings["holdings"], current_prices)
        volatility_score = calculate_volatility_score(symbols)

        risk_check = check_risk_threshold(
            portfolio_data["total_value"], volatility_score, RISK_THRESHOLDS
        )

        if risk_check["is_high_risk"]:
            report = generate_report(portfolio_data, report_format="markdown")
            send_notification(
                recipient=holdings["manager_email"], 
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
            operation="portfolio_analysis",
            details={"portfolio_id": portfolio_id, "error": str(e)},
            level="error"
        )
        print(f"Error processing portfolio {portfolio_id}: {e}")

if __name__ == "__main__":
    for portfolio in portfolios:
        analyze_portfolio(portfolio)
```


## Section 3: Design Justification

### Tool Orchestration Sequence

The sequential processing of portfolios was chosen because it allows for a clear and linear workflow. This makes the code easier to understand, debug, and maintain. While parallel processing could potentially speed up execution, the overhead of managing concurrency and synchronization might outweigh the performance benefits for this relatively small task. 

### Data Flow Strategy


The data flow strategy relies on passing outputs from one function as inputs to the next. This ensures that each step has the necessary information to complete its task correctly. For example, holdings are fetched first, then used to retrieve stock prices, which in turn are used for portfolio value calculation and volatility score determination.

### Error Handling Strategy Rationale

The `try...except` blocks with logging provide a robust error handling strategy:

- **Graceful Degradation:** If an error occurs during processing of one portfolio, the script continues to process the remaining portfolios without crashing. This ensures that as much work as possible is completed even in the presence of errors.
- **Audit Trail:** The `log_operation()` function records each major step and any encountered errors. This creates a comprehensive audit trail that can be used for debugging, monitoring, and understanding the script's behavior.

By catching exceptions specifically and logging both successes and failures, we gain valuable insights into the script's performance and potential issues.



