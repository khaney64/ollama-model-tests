## Execution Plan

1. **Initialize Configuration**
   - Tools: None
   - Set up risk thresholds and portfolio list for analysis.

2. **For Each Portfolio ID in List:**

   a. **Fetch Holdings Data**
      - Tool: `get_portfolio_holdings()`
      - Input: portfolio_id (e.g., "PORT-001")
      - Output: holdings data, which includes stock symbols needed for price fetching.
      
   b. **Get Current Stock Prices**
      - Tool: `get_stock_prices()`
      - Input: Symbols extracted from holdings data
      - Output: current prices used to calculate portfolio value and volatility.

   c. **Calculate Portfolio Value**
      - Tool: `calculate_portfolio_value()`
      - Inputs: Holdings data, current stock prices.
      - Output: Total portfolio value and position details, used for risk assessment.
   
   d. **Calculate Volatility Score**
      - Tool: `calculate_volatility_score()`
      - Input: Stock symbols from holdings
      - Output: Volatility score used to assess portfolio risk.

   e. **Check Risk Thresholds**
      - Tool: `check_risk_threshold()`
      - Inputs: Portfolio value, volatility score, and pre-defined risk configuration.
      - Output: Risk assessment results indicating if the portfolio is high-risk or not.

   f. **Generate Report for High-Risk Portfolios**
      - Tool: `generate_report()`
      - Input: Detailed portfolio data including risk level and exceeded thresholds.
      - Outputs: A markdown-formatted report to be sent in notifications.
   
   g. **Send Notification to Portfolio Manager**
      - Tool: `send_notification()`
      - Inputs: Email of the portfolio manager, report subject, report message, priority set to "high".
      - Output: Confirmation of notification being sent.

3. **Maintain Audit Trail for Operations**
   - Throughout steps a-g, use `log_operation()` to log:
     - Start and completion of analysis per portfolio
     - Results from risk threshold checks
     - Report generation status
     - Notification sending results

4. **Error Handling Strategy**
   - Wrap each step (a-g) in try/except blocks.
   - Log any errors using `log_operation()` with the level set to "error".
   - Continue processing the next portfolio if an error occurs in one, ensuring robustness.

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
import re

def analyze_portfolios():
    risk_config = {
        "max_volatility": 35.0,
        "min_value": 50000,
        "max_value": 2000000
    }
    
    portfolios = ["PORT-001", "PORT-002", "PORT-003"]

    for portfolio_id in portfolios:
        try:
            log_operation("portfolio_analysis_start", {"portfolio_id": portfolio_id}, level="info")
            
            # Step a: Fetch holdings data
            holdings_data = get_portfolio_holdings(portfolio_id)
            
            # Extract symbols from holdings data
            symbols = [holding['symbol'] for holding in holdings_data['holdings']]
            
            # Step b: Get current stock prices
            current_prices = get_stock_prices(symbols)
            
            # Filter out None prices to avoid errors in calculations
            filtered_holdings = [
                {**h, 'current_price': current_prices.get(h['symbol'])} for h in holdings_data['holdings']
                if current_prices.get(h['symbol']) is not None
            ]
            
            # Step c: Calculate portfolio value and position details
            value_data = calculate_portfolio_value(filtered_holdings, current_prices)
            
            # Step d: Calculate volatility score
            volatility_score = calculate_volatility_score(symbols)
            
            # Step e: Check risk thresholds
            risk_check = check_risk_threshold(value_data['total_value'], volatility_score, risk_config)
            
            log_operation("risk_check", {
                "portfolio_id": portfolio_id,
                "risk_level": risk_check["risk_level"]
            }, level="info")

            if risk_check["is_high_risk"]:
                # Step f: Generate report for high-risk portfolios
                report_data = {
                    "portfolio_id": holdings_data['portfolio_id'],
                    "client_name": holdings_data['client_name'],
                    "total_value": value_data['total_value'],
                    "volatility_score": volatility_score,
                    "risk_level": risk_check["risk_level"],
                    "exceeded_thresholds": risk_check["exceeded_thresholds"],
                    "positions": value_data["positions"]
                }
                
                report = generate_report(report_data, report_format="markdown")
                
                # Step g: Send notification
                send_notification(
                    recipient=holdings_data['manager_email'],
                    subject=f"High Risk Alert: Portfolio {portfolio_id}",
                    message=report,
                    priority="high"
                )
            
            log_operation("portfolio_analysis_complete", {"portfolio_id": portfolio_id}, level="info")
        
        except ValueError as ve:
            log_operation(
                "error_occurred",
                {"portfolio_id": portfolio_id, "error": str(ve)},
                level="error"
            )
        except Exception as e:
            log_operation(
                "unexpected_error",
                {"portfolio_id": portfolio_id, "error": str(e)},
                level="error"
            )

if __name__ == "__main__":
    analyze_portfolios()
```

## Design Justification

### Tool Orchestration Sequence
The orchestration follows a linear sequence for each portfolio to ensure clarity and simplicity. Each step logically builds upon the previous one, allowing data to be seamlessly passed through the process.

- **Sequential Processing**: This ensures that even if an error occurs in handling one portfolio, others can still be processed. Error logging within each portfolio's context helps identify issues without interrupting the entire batch processing.
  
### Data Flow Strategy
Data flows from fetching holdings to generating reports and sending notifications:

1. **Holdings Data** is fundamental as it feeds into both price fetching and volatility scoring steps.
2. **Current Prices** are crucial for calculating portfolio values, which are necessary before checking risk thresholds.
3. **Risk Assessment Results** determine if a report needs to be generated and sent.

This structured approach ensures that each step uses the outputs of prior operations correctly without data loss or transformation errors.

### Error Handling Strategy
Errors are caught using try/except blocks around critical steps for each portfolio:

- **Specific Exceptions**: `ValueError` is specifically handled where applicable, ensuring expected issues don't halt execution.
- **General Exception Catching**: Catches any unexpected errors to ensure robustness and continuous processing of subsequent portfolios.

### Trade-offs Considered
- **Sequential vs. Parallel Processing**: Sequential ensures easier debugging and error tracking, while parallel could increase speed but complicate handling exceptions and data consistency.
  
The design balances simplicity with functionality, ensuring the system is resilient and maintainable.

Overall, this structured approach to orchestrating tools guarantees thorough portfolio analysis, robust risk assessment, and clear reporting for high-risk portfolios.