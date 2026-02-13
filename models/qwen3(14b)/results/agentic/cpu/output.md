# Portfolio Risk Analysis Agent Implementation

## Section 1: Execution Plan

```markdown
## Execution Plan

1. **Initialize Configuration**
   - Tools: None
   - Set up risk thresholds and portfolio list
   - Define risk_config with max_volatility, min_value, and max_value

2. **For Each Portfolio:**

   a. **Fetch Holdings**
   - Tool: get_portfolio_holdings()
   - Input: portfolio_id
   - Output: holdings data (needed for steps b, c, e)
   - Error Handling: Log error and skip if portfolio not found

   b. **Extract Symbols and Get Stock Prices**
   - Tool: get_stock_prices()
   - Input: symbols from holdings
   - Output: current prices (needed for step c)
   - Error Handling: Skip symbols with unknown prices

   c. **Calculate Portfolio Value**
   - Tool: calculate_portfolio_value()
   - Input: holdings and current_prices
   - Output: total_value and position details (needed for step d)
   - Error Handling: Log error and skip if calculation fails

   d. **Calculate Volatility Score**
   - Tool: calculate_volatility_score()
   - Input: symbols from holdings
   - Output: volatility score (needed for step e)
   - Error Handling: Log error and skip if calculation fails

   e. **Check Risk Thresholds**
   - Tool: check_risk_threshold()
   - Input: total_value, volatility_score, and risk_config
   - Output: risk status (needed for step f)
   - Error Handling: Log error and skip if check fails

   f. **Generate and Send Reports for High-Risk Portfolios**
   - Tool: generate_report() and send_notification()
   - Input: portfolio_data and manager_email
   - Output: Report and notification sent
   - Error Handling: Log error if report generation or notification fails

3. **Error Handling Strategy**
   - Wrap each portfolio in try/except
   - Log errors and continue to next portfolio
   - Use specific exception handling for each tool
   - Include general exception catch-all for unexpected errors
   - Maintain audit logs for all operations
```

## Section 2: Implementation

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
from typing import Dict, List, Optional, Any

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Risk configuration thresholds
RISK_CONFIG = {
    "max_volatility": 35.0,
    "min_value": 50000,
    "max_value": 2000000
}

# List of portfolios to analyze
PORTFOLIOS_TO_ANALYZE = ["PORT-001", "PORT-002", "PORT-003"]

def analyze_portfolios():
    """Main orchestration function for portfolio risk analysis."""
    # Log start of analysis
    log_operation("portfolio_analysis_start", {"total_portfolios": len(PORTFOLIOS_TO_ANALYZE)}, "info")
    
    for portfolio_id in PORTFOLIOS_TO_ANALYZE:
        try:
            # Step 1: Get portfolio holdings
            log_operation("fetch_holdings", {"portfolio_id": portfolio_id}, "info")
            portfolio_data = get_portfolio_holdings(portfolio_id)
            
            # Step 2: Extract symbols and get stock prices
            symbols = [holding["symbol"] for holding in portfolio_data["holdings"]]
            log_operation("get_stock_prices", {"portfolio_id": portfolio_id, "symbols": symbols}, "info")
            current_prices = get_stock_prices(symbols)
            
            # Step 3: Calculate portfolio value
            log_operation("calculate_portfolio_value", {"portfolio_id": portfolio_id}, "info")
            value_data = calculate_portfolio_value(portfolio_data["holdings"], current_prices)
            
            # Step 4: Calculate volatility score
            log_operation("calculate_volatility_score", {"portfolio_id": portfolio_id, "symbols": symbols}, "info")
            volatility_score = calculate_volatility_score(symbols)
            
            # Step 5: Check risk thresholds
            log_operation("check_risk_threshold", {"portfolio_id": portfolio_id}, "info")
            risk_check = check_risk_threshold(
                value_data["total_value"],
                volatility_score,
                RISK_CONFIG
            )
            
            # Prepare portfolio data for reporting
            portfolio_report_data = {
                "portfolio_id": portfolio_id,
                "client_name": portfolio_data["client_name"],
                "total_value": value_data["total_value"],
                "volatility_score": volatility_score,
                "risk_level": risk_check["risk_level"],
                "exceeded_thresholds": risk_check["exceeded_thresholds"],
                "positions": value_data["positions"]
            }
            
            # Step 6: If high risk, generate report and send notification
            if risk_check["is_high_risk"]:
                log_operation("generate_report", {"portfolio_id": portfolio_id}, "info")
                report = generate_report(portfolio_report_data, "markdown")
                
                log_operation("send_notification", {"portfolio_id": portfolio_id}, "info")
                send_result = send_notification(
                    recipient=portfolio_data["manager_email"],
                    subject=f"High Risk Alert: Portfolio {portfolio_id}",
                    message=report,
                    priority="high"
                )
                
                # Log notification result
                log_operation("notification_sent", {
                    "portfolio_id": portfolio_id,
                    "sent": send_result["sent"],
                    "message_id": send_result["message_id"]
                }, "info")
            
            # Log completion for this portfolio
            log_operation("portfolio_analysis_complete", {
                "portfolio_id": portfolio_id,
                "risk_level": risk_check["risk_level"]
            }, "info")
            
        except ValueError as ve:
            # Handle specific value errors (e.g., invalid symbols, empty lists)
            log_operation("portfolio_analysis_error", {
                "portfolio_id": portfolio_id,
                "error_type": "ValueError",
                "message": str(ve)
            }, "warning")
            continue
        except Exception as e:
            # Handle any other unexpected errors
            log_operation("portfolio_analysis_error", {
                "portfolio_id": portfolio_id,
                "error_type": "UnexpectedError",
                "message": str(e)
            }, "error")
            continue

if __name__ == "__main__":
    analyze_portfolios()
```

## Section 3: Design Justification

```markdown
## Design Justification

### Tool Orchestration Sequence
I chose to process portfolios sequentially rather than in parallel because:
- It ensures data consistency and simplifies error handling
- Each step depends on the previous one (holdings → prices → value → volatility → risk check)
- It avoids complex concurrency patterns that could introduce race conditions

### Data Flow Strategy
Holdings data feeds into three downstream operations (price fetching, value calculation, volatility scoring) because:
- Symbols from holdings are needed for both price fetching and volatility calculation
- Holdings data is required for calculating portfolio value
- Portfolio value and volatility score are both needed for risk threshold checks
- This creates a clear dependency chain that ensures data integrity

### Error Handling Strategy
- Wrap each portfolio in a try/except block to isolate errors
- Use specific exception handling for ValueErrors (e.g., empty lists, invalid symbols)
- Log all errors with detailed context for audit purposes
- Continue processing remaining portfolios even if one fails
- Use different log levels (info, warning, error) to distinguish between normal operations and issues

### Trade-Offs Considered
- **Performance vs. Completeness**: Chose completeness over performance by processing sequentially rather than in parallel
- **Error Handling Granularity**: Added specific handling for ValueErrors while maintaining a general exception catch-all
- **Log Verbosity**: Balanced between detailed logging for audit purposes and avoiding excessive log output
- **Code Readability**: Used clear variable names and structured the code with meaningful comments
- **Error Recovery**: Chose to continue processing rather than halt on errors to ensure maximum coverage
```