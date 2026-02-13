## Section 1: Execution Plan

The goal is to build a robust Python script that orchestrates multiple tools to analyze investment portfolios, calculate risk metrics, identify high-risk portfolios, generate reports, and send notifications. Here's a step-by-step execution plan:

### Initialization
1. **Set Risk Configuration**
   - Tools: None
   - Define the `risk_config` dictionary with thresholds for volatility and portfolio values.

2. **Initialize Portfolio List**
   - Tools: None
   - Create a list of portfolios to be analyzed, e.g., ["PORT-001", "PORT-002", "PORT-003"].

### Main Processing Loop

For each portfolio in the list:

3. **Fetch Holdings**
   - Tool: `get_portfolio_holdings()`
   - Input: `portfolio_id` from the list
   - Output: Dictionary containing holdings data
   - Handle errors with try/except, log error if `ValueError` is raised.

4. **Extract Symbols and Get Current Stock Prices**
   - Tools: List comprehension for symbols extraction, `get_stock_prices()`
   - Input: Extracted symbols from holdings
   - Output: Dictionary of current stock prices
   - Handle cases where stocks may not have a price (skip these in calculations).

5. **Calculate Portfolio Value and Position Details**
   - Tool: `calculate_portfolio_value()`
   - Input: Holdings data, current stock prices
   - Output: Total portfolio value and position details
   - Skip positions with no available price data.

6. **Calculate Volatility Score**
   - Tool: `calculate_volatility_score()`
   - Input: Symbols from holdings, default 30-day period
   - Output: Float representing volatility score

7. **Check Risk Thresholds**
   - Tool: `check_risk_threshold()`
   - Input: Portfolio value, volatility score, `risk_config`
   - Output: Dictionary indicating risk status and thresholds exceeded

8. **Identify High-Risk Portfolios**
   - Conditionally proceed if portfolio is high-risk based on the output from step 7.

9. **Generate Report for High-Risk Portfolios**
   - Tool: `generate_report()`
   - Input: Portfolio data including analysis results
   - Output: Formatted report string in markdown

10. **Send Notification to Portfolio Manager**
    - Tool: `send_notification()`
    - Input: Portfolio manager's email, subject, generated report text
    - Handle errors gracefully; log notification status.

11. **Log Operations for Audit Trail**
    - Tool: `log_operation()`
    - Log each significant step with details and appropriate logging level (info/warning/error).

### Error Handling Strategy

- Each operation in the main loop is wrapped in try/except to ensure the script continues processing other portfolios if one fails.
- Errors are logged using the `log_operation()` function, providing clear audit trails of what went wrong.
- Specific errors like empty symbol lists or missing stock prices should raise and handle `ValueError`.

### Summary

This execution plan ensures that each step is clear, data dependencies are respected, and errors do not halt processing. The script maintains an audit trail for transparency and accountability.

## Section 2: Implementation (Python)

Here's the complete Python implementation based on the outlined plan:

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
import logging

# Setup basic configuration for logging
logging.basicConfig(level=logging.INFO)

def analyze_portfolios():
    """Main orchestration function to analyze portfolios."""
    
    # Initialize Risk Configuration and Portfolio List
    risk_config = {
        "max_volatility": 35.0,
        "min_value": 50000,
        "max_value": 2000000
    }
    portfolio_ids = ["PORT-001", "PORT-002", "PORT-003"]
    
    for portfolio_id in portfolio_ids:
        try:
            log_operation("portfolio_analysis_start", {"portfolio_id": portfolio_id}, level="info")
            
            # Fetch Holdings
            holdings_data = get_portfolio_holdings(portfolio_id)
            
            # Extract Symbols and Get Current Stock Prices
            symbols = [holding["symbol"] for holding in holdings_data["holdings"]]
            prices = get_stock_prices(symbols)

            # Calculate Portfolio Value
            portfolio_value_data = calculate_portfolio_value(
                holdings=holdings_data["holdings"],
                current_prices={sym: prices.get(sym) for sym in symbols if prices.get(sym) is not None}
            )
            
            # Calculate Volatility Score
            volatility_score = calculate_volatility_score(symbols=symbols)
            
            # Check Risk Thresholds
            risk_check = check_risk_threshold(
                portfolio_value=portfolio_value_data["total_value"],
                volatility_score=volatility_score,
                risk_config=risk_config
            )
            
            log_operation("risk_check", {
                "portfolio_id": portfolio_id,
                "risk_level": risk_check["risk_level"]
            }, level="info")

            # If Portfolio is High Risk, Generate Report and Send Notification
            if risk_check["is_high_risk"]:
                report_data = {
                    "portfolio_id": portfolio_id,
                    "client_name": holdings_data["client_name"],
                    "total_value": portfolio_value_data["total_value"],
                    "volatility_score": volatility_score,
                    "risk_level": risk_check["risk_level"],
                    "exceeded_thresholds": risk_check["exceeded_thresholds"],
                    "positions": portfolio_value_data["positions"]
                }
                
                report = generate_report(report_data, report_format="markdown")
                notification_result = send_notification(
                    recipient=holdings_data["manager_email"],
                    subject=f"High Risk Alert: Portfolio {portfolio_id}",
                    message=report,
                    priority="high"
                )
                
                log_operation("notification_sent", {
                    "portfolio_id": portfolio_id,
                    "sent": notification_result["sent"],
                    "message_id": notification_result.get("message_id")
                }, level="info")

        except ValueError as e:
            # Log errors and continue to next portfolio
            log_operation("error_occurred", {"portfolio_id": portfolio_id, "error_message": str(e)}, level="error")
        
        finally:
            log_operation("portfolio_analysis_complete", {"portfolio_id": portfolio_id}, level="info")

if __name__ == "__main__":
    analyze_portfolios()
```

## Section 3: Design Justification

### Tool Orchestration Sequence

The chosen sequence ensures a logical flow from fetching basic data (holdings) to complex operations (risk checks, report generation). Each step's output becomes an input for the next, maintaining coherence and consistency in data handling.

### Data Flow Strategy

Data is passed sequentially through the pipeline with clear dependencies: holdings feed into price calculations; these results inform value and volatility assessments. Handling stock prices cautiously ensures no disruptions due to missing or `None` values, allowing operations like portfolio valuation to skip invalid entries without failing.

### Error Handling Strategy

Using try/except blocks around each major operation allows for robust error handling without halting the entire process. This approach ensures that even if one portfolio analysis encounters issues (e.g., data fetch errors), others can proceed uninterrupted. Logging these occurrences provides transparency and aids in troubleshooting, while finally blocks ensure all operations conclude with appropriate logging.

### Trade-offs Considered

- **Sequential vs. Parallel Processing**: Sequential processing was chosen for simplicity and to prevent race conditions or complex synchronization needs, which might complicate error handling.
  
- **Error Handling Granularity**: The script opts for fine-grained try/except blocks around each tool call to handle specific errors without affecting others.

By following this design, the script remains robust, flexible, and easy to maintain, while ensuring comprehensive processing of portfolios as required.