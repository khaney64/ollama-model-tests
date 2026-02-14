## Execution Plan (Markdown)

### Introduction
This execution plan outlines the step-by-step process of analyzing multiple investment portfolios using the provided toolkit. The goal is to calculate risk metrics, identify high-risk portfolios, generate reports, and send notifications to portfolio managers.

### Step-by-Step Breakdown

1. **Initialize Configuration**
   - Tools: None
   - Set up the list of portfolios to be analyzed and configure the risk thresholds.
   - Example:
     ```python
     PORTFOLIOS = ["PORT-001", "PORT-002", "PORT-003"]
     RISK_CONFIG = {
         "max_volatility": 35.0,
         "min_value": 50000,
         "max_value": 2000000
     }
     ```

2. **For Each Portfolio:**

   a. **Fetch Holdings**
      - Tool: `get_portfolio_holdings()`
      - Input: portfolio_id
      - Output: holdings data (used for steps b, c, e)
      - Example:
        ```python
        try:
            portfolio = get_portfolio_holdings(portfolio_id)
        except ValueError as e:
            log_operation("portfolio_fetch", {"portfolio_id": portfolio_id}, "error")
            print(f"Failed to fetch holdings for {portfolio_id}: {e}")
            continue
        ```

   b. **Get Stock Prices**
      - Tool: `get_stock_prices()`
      - Input: symbols from the portfolio's holdings
      - Output: current prices (used for steps c)
      - Example:
        ```python
        symbols = [item['symbol'] for item in portfolio['holdings']]
        try:
            prices = get_stock_prices(symbols)
        except ValueError as e:
            log_operation("price_fetch", {"portfolio_id": portfolio_id}, "error")
            print(f"Failed to fetch stock prices for {portfolio_id}: {e}")
            continue
        ```

   c. **Calculate Portfolio Value**
      - Tool: `calculate_portfolio_value()`
      - Input: holdings data and current prices
      - Output: calculated portfolio value, positions details (used for steps d)
      - Example:
        ```python
        try:
            value_data = calculate_portfolio_value(portfolio['holdings'], prices)
        except ValueError as e:
            log_operation("value_calc", {"portfolio_id": portfolio_id}, "error")
            print(f"Failed to calculate values for {portfolio_id}: {e}")
            continue
        ```

   d. **Calculate Volatility Score**
      - Tool: `calculate_volatility_score()`
      - Input: symbols from the portfolio's holdings (used in step e)
      - Output: volatility score (used for step e)
      - Example:
        ```python
        try:
            volatility = calculate_volatility_score(symbols, days=30)
        except ValueError as e:
            log_operation("volatility_calc", {"portfolio_id": portfolio_id}, "error")
            print(f"Failed to calculate volatility for {portfolio_id}: {e}")
            continue
        ```

   e. **Check Risk Thresholds**
      - Tool: `check_risk_threshold()`
      - Input: calculated value data and volatility score, risk thresholds
      - Output: risk assessment (used for steps f, g)
      - Example:
        ```python
        try:
            risk_result = check_risk_threshold(value_data['total_value'], volatility, RISK_CONFIG)
        except ValueError as e:
            log_operation("risk_check", {"portfolio_id": portfolio_id}, "error")
            print(f"Failed to check risk thresholds for {portfolio_id}: {e}")
            continue
        ```

   f. **Generate and Send Report**
      - Tool: `generate_report()`
      - Input: combined analysis data
      - Output: report text (used in step g)
      - Example:
        ```python
        try:
            report_text = generate_report({
                "portfolio_id": portfolio['portfolio_id'],
                "client_name": portfolio['client_name'],
                "total_value": value_data['total_value'],
                "volatility_score": volatility,
                "risk_level": risk_result['risk_level'],
                "exceeded_thresholds": risk_result['exceeded_thresholds'],
                "positions": value_data['positions']
            })
        except ValueError as e:
            log_operation("report_gen", {"portfolio_id": portfolio_id}, "error")
            print(f"Failed to generate report for {portfolio_id}: {e}")
            continue
        ```

   g. **Send Notification**
      - Tool: `send_notification()`
      - Input: recipient email, report text
      - Output: notification result (logged in step f)
      - Example:
        ```python
        try:
            send_result = send_notification(
                portfolio['manager_email'],
                "High Risk Alert: Portfolio " + portfolio['portfolio_id'],
                report_text,
                priority="high"
            )
            log_operation("notification_sent", {
                "portfolio_id": portfolio['portfolio_id'],
                "message_id": send_result['message_id'],
                "timestamp": send_result['timestamp']
            }, level="info")
        except ValueError as e:
            log_operation("notification_failed", {"portfolio_id": portfolio_id}, "error")
            print(f"Failed to send notification for {portfolio_id}: {e}")
    ```

3. **Error Handling Strategy**
   - Wrap each operation in try/except blocks
   - Log errors and continue processing the next portfolio
   - Example:
     ```python
     try:
         analyze_portfolios()
     except Exception as e:
         log_operation("script_error", {"error": str(e)}, "critical")
         print(f"Script execution failed with error: {e}")
     ```

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
    PORTFOLIOS = ["PORT-001", "PORT-002", "PORT-003"]
    RISK_CONFIG = {
        "max_volatility": 35.0,
        "min_value": 50000,
        "max_value": 2000000
    }

    for portfolio_id in PORTFOLIOS:
        log_operation("portfolio_analysis_start", {"portfolio_id": portfolio_id})

        try:
            # Step 1: Fetch Holdings
            portfolio = get_portfolio_holdings(portfolio_id)
        except ValueError as e:
            log_operation("portfolio_fetch", {"portfolio_id": portfolio_id}, "error")
            print(f"Failed to fetch holdings for {portfolio_id}: {e}")
            continue

        symbols = [item['symbol'] for item in portfolio['holdings']]
        
        # Step 2: Get Stock Prices
        try:
            prices = get_stock_prices(symbols)
        except ValueError as e:
            log_operation("price_fetch", {"portfolio_id": portfolio_id}, "error")
            print(f"Failed to fetch stock prices for {portfolio_id}: {e}")
            continue

        # Step 3: Calculate Portfolio Value
        try:
            value_data = calculate_portfolio_value(portfolio['holdings'], prices)
        except ValueError as e:
            log_operation("value_calc", {"portfolio_id": portfolio_id}, "error")
            print(f"Failed to calculate values for {portfolio_id}: {e}")
            continue

        # Step 4: Calculate Volatility Score
        try:
            volatility = calculate_volatility_score(symbols, days=30)
        except ValueError as e:
            log_operation("volatility_calc", {"portfolio_id": portfolio_id}, "error")
            print(f"Failed to calculate volatility for {portfolio_id}: {e}")
            continue

        # Step 5: Check Risk Thresholds
        try:
            risk_result = check_risk_threshold(value_data['total_value'], volatility, RISK_CONFIG)
        except ValueError as e:
            log_operation("risk_check", {"portfolio_id": portfolio_id}, "error")
            print(f"Failed to check risk thresholds for {portfolio_id}: {e}")
            continue

        # Step 6: Generate and Send Report
        try:
            report_text = generate_report({
                "portfolio_id": portfolio['portfolio_id'],
                "client_name": portfolio['client_name'],
                "total_value": value_data['total_value'],
                "volatility_score": volatility,
                "risk_level": risk_result['risk_level'],
                "exceeded_thresholds": risk_result['exceeded_thresholds'],
                "positions": value_data['positions']
            })
        except ValueError as e:
            log_operation("report_gen", {"portfolio_id": portfolio_id}, "error")
            print(f"Failed to generate report for {portfolio_id}: {e}")
            continue

        try:
            send_result = send_notification(
                portfolio['manager_email'],
                "High Risk Alert: Portfolio " + portfolio['portfolio_id'],
                report_text,
                priority="high"
            )
            log_operation("notification_sent", {
                "portfolio_id": portfolio['portfolio_id'],
                "message_id": send_result['message_id'],
                "timestamp": send_result['timestamp']
            }, level="info")
        except ValueError as e:
            log_operation("notification_failed", {"portfolio_id": portfolio_id}, "error")
            print(f"Failed to send notification for {portfolio_id}: {e}")

        log_operation("portfolio_analysis_end", {"portfolio_id": portfolio_id})

if __name__ == "__main__":
    try:
        analyze_portfolios()
    except Exception as e:
        log_operation("script_error", {"error": str(e)}, "critical")
        print(f"Script execution failed with error: {e}")
```

## Design Justification (Markdown)

### Tool Orchestration Sequence
I chose to process portfolios sequentially rather than in parallel because each portfolio relies on data from previous steps. Parallel processing would require more complex synchronization mechanisms and could introduce race conditions. By ensuring a linear flow, we can simplify the implementation and avoid potential issues.

### Data Flow Strategy
Holdings data feeds into three downstream operations: fetching stock prices, calculating portfolio value, and computing volatility scores. This modular approach ensures that each step's output is correctly passed to the next step, maintaining data integrity throughout the process.

### Error Handling Strategy
I included comprehensive try/except blocks around each major operation. If an error occurs, it logs the error with a detailed message, indicating which portfolio caused the issue and what went wrong. This allows for easy troubleshooting without interrupting the processing of other portfolios. The script continues to execute, ensuring that all available portfolios are processed even if one fails.

### Trade-offs Considered
- **Simplicity vs. Parallelism**: Sequential execution is simpler and less error-prone compared to parallel processing.
- **Resource Utilization**: Sequential processing uses fewer system resources since there's no need for complex synchronization mechanisms.
- **Maintainability**: Linear flow makes it easier to understand, debug, and modify the script.

In summary, this design balances simplicity, reliability, and resource efficiency while ensuring that all specified requirements are met.