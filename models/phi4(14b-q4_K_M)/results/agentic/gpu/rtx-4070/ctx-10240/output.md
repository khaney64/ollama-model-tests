# Section 1: Execution Plan

## Overview

The goal is to create a script that orchestrates multiple tools to analyze investment portfolios, calculate risk metrics, identify high-risk portfolios, generate reports, send notifications, and log operations. The system will process three specific portfolios with defined risk thresholds.

## Step-by-Step Execution Plan

### 1. **Initialize Configuration**
   - Tools: None
   - Set up risk thresholds and define the list of portfolio IDs (`PORT-001`, `PORT-002`, `PORT-003`).
   - Ensure all necessary configurations are in place before processing portfolios.

### 2. **For Each Portfolio:**

#### a. **Fetch Holdings**
   - Tool: `get_portfolio_holdings()`
   - Input: `portfolio_id`
   - Output: holdings data
   - Data Dependencies: Required for subsequent steps that need portfolio details.

#### b. **Get Stock Prices**
   - Tool: `get_stock_prices()`
   - Input: Symbols extracted from holdings
   - Output: Current prices dictionary
   - Data Dependencies: Use symbols from the fetched holdings to get current market prices.

#### c. **Calculate Portfolio Value**
   - Tool: `calculate_portfolio_value()`
   - Inputs: Holdings data, Current prices dictionary
   - Output: Total portfolio value and position details
   - Data Dependencies: Requires both current prices and holding information.

#### d. **Calculate Volatility Score**
   - Tool: `calculate_volatility_score()`
   - Input: Symbols extracted from holdings
   - Output: Portfolio volatility score
   - Data Dependencies: Use symbols to determine how volatile the portfolio is over a 30-day period.

### 3. **Apply Risk Configuration**

#### e. **Check Risk Threshold**
   - Tool: `check_risk_threshold()`
   - Inputs: Calculated portfolio value, Volatility score, Risk configuration
   - Output: Dictionary indicating if thresholds are exceeded and risk level
   - Data Dependencies: Relies on the calculated values from steps c and d.

### 4. **Identify High-Risk Portfolios**

#### f. **Decision Making**
   - Check if a portfolio is high-risk based on the output of step e.
   - If it is, proceed to generate reports and send notifications.

### 5. **Generate and Send Reports for High-Risk Portfolios**

#### g. **Generate Report**
   - Tool: `generate_report()`
   - Input: Portfolio analysis data
   - Output: Formatted markdown report
   - Data Dependencies: Requires complete portfolio data, including risk level and exceeded thresholds.

#### h. **Send Notification**
   - Tool: `send_notification()`
   - Inputs: Manager's email from holdings, Report subject, Message content (report), Priority set to "high"
   - Output: Confirmation of notification sent
   - Data Dependencies: Uses the generated report as message content and portfolio manager details.

### 6. **Maintain Audit Trail**

#### i. **Log Operations**
   - Tool: `log_operation()`
   - Input: Details about each major operation (e.g., fetching holdings, calculating risk)
   - Output: None (logs to system)
   - Data Dependencies: Logs must capture essential details for all significant actions taken during processing.

### 7. **Handle Errors Gracefully**

- Wrap operations within `try/except` blocks to catch specific exceptions.
- Log errors with appropriate log levels and continue processing other portfolios if one fails.
- Ensure the script can recover or skip problematic steps without halting the entire process.

# Section 2: Implementation (Python)

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

def analyze_portfolios():
    """Main orchestration function."""
    
    # Risk configuration setup
    risk_config = {
        "max_volatility": 35.0,
        "min_value": 50000,
        "max_value": 2000000
    }
    
    portfolio_ids = ["PORT-001", "PORT-002", "PORT-003"]
    
    for portfolio_id in portfolio_ids:
        try:
            log_operation("portfolio_analysis_start", {"portfolio_id": portfolio_id}, level="info")
            
            # Step a: Fetch Holdings
            holdings_data = get_portfolio_holdings(portfolio_id)
            symbols = [holding['symbol'] for holding in holdings_data['holdings']]
            
            # Step b: Get Stock Prices
            current_prices = get_stock_prices(symbols)
            
            # Step c: Calculate Portfolio Value
            portfolio_value_data = calculate_portfolio_value(holdings_data['holdings'], current_prices)
            
            # Step d: Calculate Volatility Score
            volatility_score = calculate_volatility_score(symbols, days=30)
            
            # Step e: Check Risk Threshold
            risk_check_result = check_risk_threshold(
                portfolio_value_data["total_value"],
                volatility_score,
                risk_config
            )
            
            log_operation("risk_check", {
                "portfolio_id": portfolio_id,
                "is_high_risk": risk_check_result["is_high_risk"]
            }, level="info" if not risk_check_result["is_high_risk"] else "warning")
            
            # Step f: Identify High-Risk Portfolios
            if risk_check_result["is_high_risk"]:
                # Step g: Generate Report
                report_data = {
                    "portfolio_id": portfolio_id,
                    "client_name": holdings_data['client_name'],
                    "total_value": portfolio_value_data["total_value"],
                    "volatility_score": volatility_score,
                    "risk_level": risk_check_result["risk_level"],
                    "exceeded_thresholds": risk_check_result["exceeded_thresholds"],
                    "positions": portfolio_value_data["positions"]
                }
                
                report = generate_report(report_data, report_format="markdown")
                
                # Step h: Send Notification
                notification_result = send_notification(
                    recipient=holdings_data['manager_email'],
                    subject=f"High Risk Alert: Portfolio {portfolio_id}",
                    message=report,
                    priority="high"
                )
                
                log_operation("notification_sent", {
                    "portfolio_id": portfolio_id,
                    "message_id": notification_result["message_id"],
                    "timestamp": notification_result["timestamp"]
                }, level="info")
            
            log_operation("portfolio_analysis_completion", {"portfolio_id": portfolio_id}, level="info")

        except ValueError as ve:
            log_operation("error_encountered", {
                "portfolio_id": portfolio_id,
                "error": str(ve)
            }, level="error")
        except Exception as e:
            log_operation("unexpected_error", {
                "portfolio_id": portfolio_id,
                "error": str(e)
            }, level="error")

if __name__ == "__main__":
    analyze_portfolios()
```

# Section 3: Design Justification

### Tool Orchestration Sequence
The choice to process portfolios sequentially allows for easy tracking and logging of each portfolio's analysis, including handling errors specific to each one. This step-by-step approach is crucial for maintaining clarity in audit trails and ensuring that issues with one portfolio do not affect the others.

### Data Flow Strategy
Data is passed directly from one tool to another based on dependencies outlined in the execution plan. For instance, holdings data feeds into stock price retrieval, which then informs value calculations. This ensures efficient use of data without unnecessary recomputation or re-fetching.

### Error Handling Strategy
Each major step within a portfolio's analysis is wrapped in `try/except` blocks to catch specific errors (e.g., `ValueError`) and log them appropriately. The strategy allows the script to continue processing other portfolios even if one fails, ensuring robustness and continuity of operation.

### Trade-offs Considered
- **Sequential vs. Parallel Processing:** Sequential processing was chosen for its simplicity in managing error logging and audit trails compared to parallel execution.
- **Error Handling Granularity:** Errors are logged at both specific operations and portfolio levels to ensure detailed traceability without cluttering logs with repetitive information. 

This design balances clarity, maintainability, and robustness while achieving the task's objectives effectively.