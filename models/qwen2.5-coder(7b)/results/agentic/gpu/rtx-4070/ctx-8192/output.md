## Execution Plan (Markdown)

### Step-by-Step Execution Plan

1. **Initialize Configuration**
   - Tools: None
   - Set up risk thresholds and portfolio list
   - Example:
     ```python
     risk_config = {
         "max_volatility": 35.0,
         "min_value": 50000,
         "max_value": 2000000
     }
     portfolios = ["PORT-001", "PORT-002", "PORT-003"]
     ```

2. **For Each Portfolio:**

   a. **Fetch Holdings**
   - Tool: `get_portfolio_holdings()`
   - Input: `portfolio_id` (e.g., `"PORT-001"`)
   - Output: Holdings data (needed for steps b, c, e)
     ```python
     holdings = get_portfolio_holdings("PORT-001")
     ```

   b. **Get Stock Prices**
   - Tool: `get_stock_prices()`
   - Input: Symbols extracted from holdings
   - Output: Current prices (needed for step c)
     ```python
     symbols = [holding["symbol"] for holding in holdings["holdings"]]
     stock_prices = get_stock_prices(symbols)
     ```

   c. **Calculate Portfolio Value and Positions**
   - Tool: `calculate_portfolio_value()`
   - Input: Holdings data and current prices
   - Output: Total portfolio value and position details
     ```python
     portfolio_value_data = calculate_portfolio_value(holdings["holdings"], stock_prices)
     ```

   d. **Calculate Volatility Score**
   - Tool: `calculate_volatility_score()`
   - Input: Symbols extracted from holdings (for 30-day period)
   - Output: Volatility score
     ```python
     portfolio_symbols = [holding["symbol"] for holding in holdings["holdings"]]
     volatility_score = calculate_volatility_score(portfolio_symbols, days=30)
     ```

   e. **Check Risk Thresholds**
   - Tool: `check_risk_threshold()`
   - Input: Portfolio value and volatility score
   - Output: Whether portfolio exceeds risk thresholds
     ```python
     risk_check_result = check_risk_threshold(portfolio_value_data["total_value"], volatility_score, risk_config)
     ```

   f. **Generate Report (if high-risk)**
   - Tool: `generate_report()`
   - Input: Portfolio data and report format ("markdown")
   - Output: Formatted report string
     ```python
     if risk_check_result["is_high_risk"]:
         report = generate_report(portfolio_value_data, "markdown")
     ```

   g. **Send Notification (if high-risk)**
   - Tool: `send_notification()`
   - Input: Manager's email, subject, message, and priority ("high")
   - Output: Confirmation of notification sent
     ```python
     if risk_check_result["is_high_risk"]:
         send_notification(holdings["manager_email"], "High Risk Alert: Portfolio PORT-001", report)
     ```

3. **Error Handling Strategy**
   - Wrap each portfolio in `try/except` blocks to handle errors gracefully.
   - Log errors and continue processing remaining portfolios.

4. **Maintain Audit Trail**
   - Log all major operations (portfolio analysis, risk check, report generation, notification sending).

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
            log_operation("portfolio_analysis_start", {"portfolio_id": portfolio_id}, level="info")
            
            # Step 2a: Fetch Holdings
            holdings = get_portfolio_holdings(portfolio_id)
            log_operation("holdings_fetched", {"portfolio_id": portfolio_id}, level="info")

            symbols = [holding["symbol"] for holding in holdings["holdings"]]
            
            # Step 2b: Get Stock Prices
            stock_prices = get_stock_prices(symbols)
            log_operation("stock_prices_fetched", {"portfolio_id": portfolio_id}, level="info")

            # Step 2c: Calculate Portfolio Value and Positions
            portfolio_value_data = calculate_portfolio_value(holdings["holdings"], stock_prices)
            log_operation("portfolio_value_calculated", {"portfolio_id": portfolio_id, "value": portfolio_value_data["total_value"]}, level="info")

            # Step 2d: Calculate Volatility Score
            volatility_score = calculate_volatility_score(symbols, days=30)
            log_operation("volatility_score_calculated", {"portfolio_id": portfolio_id, "score": volatility_score}, level="info")
            
            # Step 2e: Check Risk Thresholds
            risk_check_result = check_risk_threshold(portfolio_value_data["total_value"], volatility_score, risk_config)
            log_operation("risk_threshold_checked", {"portfolio_id": portfolio_id, "is_high_risk": risk_check_result["is_high_risk"]}, level="info")

            if risk_check_result["is_high_risk"]:
                # Step 2f: Generate Report
                report = generate_report(portfolio_value_data, "markdown")
                log_operation("report_generated", {"portfolio_id": portfolio_id}, level="info")

                # Step 2g: Send Notification
                send_notification(
                    holdings["manager_email"],
                    "High Risk Alert: Portfolio PORT-001",
                    report,
                    priority="high"
                )
                log_operation("notification_sent", {"portfolio_id": portfolio_id, "recipient": holdings["manager_email"]}, level="info")

            log_operation("portfolio_analysis_end", {"portfolio_id": portfolio_id}, level="info")

        except Exception as e:
            log_operation("error_occurred", {"portfolio_id": portfolio_id, "error": str(e)}, level="error")
            print(f"An error occurred while processing portfolio {portfolio_id}: {e}")

if __name__ == "__main__":
    analyze_portfolios()
```

## Design Justification (Markdown)

### Tool Orchestration Sequence
I chose to process portfolios sequentially rather than in parallel because each step depends on the previous one. For example, fetching stock prices requires the current holdings data, and generating a report relies on both portfolio value data and risk check results.

### Data Flow Strategy
Holdings data feeds into three downstream operations (price fetching, value calculation, volatility scoring) because these steps are logically dependent and produce intermediate results that are required for subsequent steps. For instance, price fetching is necessary to calculate portfolio value, which in turn is needed to generate a detailed report.

### Error Handling Strategy Rationale
Error handling is crucial here to ensure robustness and reliability of the system. By wrapping each portfolio processing step in `try/except` blocks, I can catch any exceptions that occur during execution and log them without terminating the entire script. This allows for graceful degradation and ensures that as much processing as possible is completed.

### Trade-offs Considered
- **Concurrency vs. Sequential Processing**: While parallel processing could potentially speed up the overall time, it adds complexity and increases the risk of race conditions or data inconsistencies.
- **Error Robustness**: By prioritizing error handling and logging, we ensure that even in the face of failures, all operations are recorded, allowing for recovery and analysis.

This design ensures a comprehensive and reliable solution to the task at hand.