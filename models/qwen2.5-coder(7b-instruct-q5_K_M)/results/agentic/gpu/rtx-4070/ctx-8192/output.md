## Execution Plan (Markdown)

### Step-by-Step Plan

1. **Initialize Configuration**
   - Tools: None
   - Set up risk thresholds and portfolio list:
     ```python
     RISK_CONFIG = {
         "max_volatility": 35.0,
         "min_value": 50000,
         "max_value": 2000000
     }
     PORTFOLIOS = ["PORT-001", "PORT-002", "PORT-003"]
     ```

2. **For Each Portfolio:**
   - a. **Fetch Holdings**
      - Tool: `get_portfolio_holdings()`
      - Input: portfolio_id
      - Output: holdings data (needed for steps b, c, e)
   - b. **Get Stock Prices**
      - Tool: `get_stock_prices()`
      - Input: symbols extracted from holdings
      - Output: current prices (needed for step c)
   - c. **Calculate Portfolio Value and Positions**
      - Tool: `calculate_portfolio_value()`
      - Input: holdings, current prices
      - Output: portfolio value, individual position details
   - d. **Calculate Volatility Score**
      - Tool: `calculate_volatility_score()`
      - Input: symbols from holdings, 30 days
      - Output: volatility score
   - e. **Check Risk Thresholds**
      - Tool: `check_risk_threshold()`
      - Input: portfolio value, volatility score, RISK_CONFIG
      - Output: whether risk thresholds are exceeded and risk level

3. **Identify High-Risk Portfolios**
   - Filter portfolios that return `is_high_risk` as `True`

4. **Generate and Send Reports**
   - For each high-risk portfolio:
     - a. **Generate Report**
        - Tool: `generate_report()`
        - Input: portfolio data (from step e), report format "markdown"
        - Output: markdown-formatted report
     - b. **Send Notification**
        - Tool: `send_notification()`
        - Input: manager's email, subject, report text, priority "high"
        - Output: notification result

5. **Maintain Audit Trail**
   - Log each major operation using `log_operation()`:
     - Portfolio analysis start/completion
     - Risk threshold checks
     - Report generation
     - Notification sending

6. **Error Handling Strategy**
   - Wrap each portfolio in try/except blocks to catch and log any errors.
   - Continue processing remaining portfolios even if one fails.

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
    RISK_CONFIG = {
        "max_volatility": 35.0,
        "min_value": 50000,
        "max_value": 2000000
    }
    PORTFOLIOS = ["PORT-001", "PORT-002", "PORT-003"]

    for portfolio_id in PORTFOLIOS:
        try:
            # Step a: Fetch Holdings
            log_operation("fetch_holdings", {"portfolio_id": portfolio_id}, level="info")
            holdings = get_portfolio_holdings(portfolio_id)

            # Step b: Get Stock Prices
            symbols = [holding["symbol"] for holding in holdings["holdings"]]
            log_operation("get_stock_prices", {"symbols": symbols}, level="info")
            prices = get_stock_prices(symbols)

            # Step c: Calculate Portfolio Value and Positions
            log_operation("calculate_portfolio_value", {"portfolio_id": portfolio_id, "symbols": symbols}, level="info")
            value_data = calculate_portfolio_value(holdings["holdings"], prices)

            # Step d: Calculate Volatility Score
            log_operation("calculate_volatility_score", {"symbols": symbols, "days": 30}, level="info")
            volatility = calculate_volatility_score(symbols, days=30)

            # Step e: Check Risk Thresholds
            log_operation("check_risk_threshold", {
                "portfolio_id": portfolio_id,
                "portfolio_value": value_data["total_value"],
                "volatility_score": volatility,
                "risk_config": RISK_CONFIG
            }, level="info")
            risk_check = check_risk_threshold(value_data["total_value"], volatility, RISK_CONFIG)

            # Step 4: Identify High-Risk Portfolios
            if risk_check["is_high_risk"]:
                portfolio_details = {
                    "portfolio_id": portfolio_id,
                    "client_name": holdings["client_name"],
                    "total_value": value_data["total_value"],
                    "volatility_score": volatility,
                    "risk_level": risk_check["risk_level"],
                    "exceeded_thresholds": risk_check["exceeded_thresholds"],
                    "positions": value_data["positions"]
                }

                # Step 5: Generate and Send Reports
                log_operation("generate_report", {"portfolio_id": portfolio_id}, level="info")
                report_text = generate_report(portfolio_details, report_format="markdown")

                log_operation("send_notification", {
                    "recipient": holdings["manager_email"],
                    "subject": f"High Risk Alert: Portfolio {portfolio_id}",
                    "message": report_text,
                    "priority": "high"
                }, level="info")
                result = send_notification(
                    recipient=holdings["manager_email"],
                    subject=f"High Risk Alert: Portfolio {portfolio_id}",
                    message=report_text,
                    priority="high"
                )

        except Exception as e:
            log_operation("error", {"operation": "analyze_portfolios", "details": str(e)}, level="error")
            print(f"An error occurred while processing portfolio {portfolio_id}: {e}")

if __name__ == "__main__":
    analyze_portfolios()
```

## Design Justification (Markdown)

### Tool Orchestration Sequence
I chose to process portfolios sequentially rather than in parallel because:
- Sequential processing ensures that each step completes before moving on to the next, avoiding potential data inconsistencies or race conditions.
- It simplifies error handling by allowing easy identification of which portfolio failed.

### Data Flow Strategy
Holdings data feeds into three downstream operations (price fetching, value calculation, volatility scoring) because:
- The dependencies are clear: stock prices need holdings data, value calculations need both holdings and prices, and volatility scoring needs only the symbols from holdings.
- This modular approach makes each step easier to test and maintain independently.

### Error Handling Strategy Rationale
I used comprehensive try/except blocks around each portfolio processing to catch and log any errors. This allows for graceful degradation, ensuring that the entire script can continue even if one portfolio fails. By logging errors at various points in the process (fetching holdings, calculating values, etc.), we maintain an audit trail of what went wrong during execution.

### Trade-offs Considered
- **Simplicity vs. Parallelism**: While parallel processing could potentially speed up the overall runtime, it adds complexity and requires careful management to avoid race conditions.
- **Resource Usage**: Sequential processing is more resource-efficient as each task completes before starting the next, reducing the risk of resource contention.

Overall, this sequential approach provides a balance between simplicity, robustness, and ease of maintenance.