## Execution Plan

### Step-by-Step Plan

1. **Initialize Configuration**
   - Tools: None
   - Set up risk thresholds and portfolio list.

2. **For Each Portfolio:**

   a. **Fetch Holdings**
      - Tool: `get_portfolio_holdings()`
      - Input: `portfolio_id`
      - Output: Holdings data (needed for steps b, c, e)

   b. **Get Stock Prices**
      - Tool: `get_stock_prices()`
      - Input: Symbols extracted from holdings
      - Output: Current prices (needed for step c)

   c. **Calculate Portfolio Value and Positions**
      - Tool: `calculate_portfolio_value()`
      - Inputs: Holdings, current prices
      - Output: Calculated portfolio value and positions details

   d. **Calculate Volatility Score**
      - Tool: `calculate_volatility_score()`
      - Input: Symbols from holdings, days for volatility score (default 30)
      - Output: Volatility score

   e. **Check Risk Thresholds**
      - Tool: `check_risk_threshold()`
      - Inputs: Total portfolio value, volatility score, risk configuration
      - Output: Risk level and thresholds exceeded

   f. **Generate Report for High-Risk Portfolios**
      - Tool: `generate_report()`
      - Input: Portfolio data with calculated values and positions
      - Output: Markdown-formatted report (needed for step g)

   g. **Send Notification for High-Risk Portfolios**
      - Tool: `send_notification()`
      - Inputs: Recipient, subject, message, priority ("high")
      - Output: Sending result

3. **Maintain Audit Trail**
   - Tool: `log_operation()`
   - Inputs: Operation name and details
   - Output: None (logs to system)

4. **Error Handling Strategy**
   - Wrap each portfolio in a try/except block.
   - Log errors and continue processing the next portfolio.

## Implementation

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
    # Step 1: Initialize Configuration
    risk_config = {
        "max_volatility": 35.0,
        "min_value": 50000,
        "max_value": 2000000
    }
    portfolios = ["PORT-001", "PORT-002", "PORT-003"]

    # Step 2: For Each Portfolio
    for portfolio_id in portfolios:
        try:
            log_operation("portfolio_analysis_start", {"portfolio_id": portfolio_id})

            # a. Fetch Holdings
            holdings = get_portfolio_holdings(portfolio_id)
            if not holdings:
                raise ValueError(f"No holdings found for {portfolio_id}")

            symbols = [holding["symbol"] for holding in holdings["holdings"]]
            log_operation("fetched_holdings", {"portfolio_id": portfolio_id, "symbols": symbols})

            # b. Get Stock Prices
            prices = get_stock_prices(symbols)
            if not all(prices.values()):
                raise ValueError(f"Missing stock price data for {portfolio_id}")

            log_operation("fetched_stock_prices", {"portfolio_id": portfolio_id, "prices": prices})

            # c. Calculate Portfolio Value and Positions
            portfolio_value_data = calculate_portfolio_value(holdings["holdings"], prices)
            if not portfolio_value_data:
                raise ValueError(f"No position value data for {portfolio_id}")

            log_operation("calculated_portfolio_value", {"portfolio_id": portfolio_id, "value_data": portfolio_value_data})

            # d. Calculate Volatility Score
            volatility_score = calculate_volatility_score(symbols, days=30)
            if not 0 <= volatility_score <= 100:
                raise ValueError(f"Invalid volatility score for {portfolio_id}")

            log_operation("calculated_volatility_score", {"portfolio_id": portfolio_id, "volatility_score": volatility_score})

            # e. Check Risk Thresholds
            risk_check = check_risk_threshold(
                portfolio_value=portfolio_value_data["total_value"],
                volatility_score=volatility_score,
                risk_config=risk_config
            )
            if not isinstance(risk_check, dict):
                raise ValueError(f"Invalid risk check result for {portfolio_id}")

            log_operation("checked_risk_thresholds", {"portfolio_id": portfolio_id, "risk_check": risk_check})

            # f. Generate Report for High-Risk Portfolios
            if risk_check["is_high_risk"]:
                report_data = {
                    **holdings,
                    "total_value": portfolio_value_data["total_value"],
                    "volatility_score": volatility_score,
                    "positions": [position for position in portfolio_value_data["positions"] if position],
                    "risk_level": risk_check["risk_level"],
                    "exceeded_thresholds": risk_check["exceeded_thresholds"]
                }
                report = generate_report(report_data, report_format="markdown")
                if not isinstance(report, str):
                    raise ValueError(f"Invalid report for {portfolio_id}")

                log_operation("generated_report", {"portfolio_id": portfolio_id, "report": report})

                # g. Send Notification for High-Risk Portfolios
                notification_result = send_notification(
                    recipient=holdings["manager_email"],
                    subject=f"High Risk Alert: Portfolio {portfolio_id}",
                    message=report,
                    priority="high"
                )
                if not isinstance(notification_result, dict) or not notification_result.get("sent", False):
                    raise ValueError(f"Notification failed for {portfolio_id}")

                log_operation("sent_notification", {"portfolio_id": portfolio_id, "notification_result": notification_result})
            else:
                # Log non-high-risk portfolios
                log_operation("non_high_risk_portfolio", {"portfolio_id": portfolio_id})

        except Exception as e:
            print(f"Error analyzing {portfolio_id}: {e}")
            log_operation("error_analyzing_portfolio", {"portfolio_id": portfolio_id, "exception": str(e)})

# Entry point
if __name__ == "__main__":
    analyze_portfolios()
```

## Design Justification

### Tool Orchestration Sequence
I chose to process portfolios sequentially rather than in parallel because the dependencies between steps make it easier to manage and ensure that each step is completed before moving on. This approach also simplifies error handling, as we can catch issues at any point and log them without needing to worry about concurrent operations.

### Data Flow Strategy
Holdings data feeds into three downstream operations (price fetching, value calculation, volatility scoring) because these steps are necessary for calculating risk metrics. The calculated portfolio values and positions from step c are used in generating the report in step f, which is crucial for creating a detailed analysis. Similarly, the volatility score from step d is essential for determining if a portfolio exceeds risk thresholds in step e.

### Error Handling Strategy
I wrapped each portfolio processing block in a try/except structure to handle potential errors gracefully. This ensures that we can log any issues and continue with the next portfolio, preventing the entire process from failing due to a single error. Additionally, logging is done at multiple points throughout the script to maintain an audit trail of all operations.

### Trade-offs Considered
- **Simplicity vs. Parallelism**: Choosing sequential processing over parallel execution simplifies the code and reduces complexity, making it easier to understand and maintain.
- **Error Handling**: While this approach may introduce some overhead in terms of logging, it ensures robustness and traceability, which are critical for production environments.

This design balances simplicity with robust error handling and data flow management, ensuring that the script can handle errors gracefully while maintaining a clear audit trail.