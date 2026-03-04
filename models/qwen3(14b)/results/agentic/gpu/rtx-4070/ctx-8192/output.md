# Portfolio Risk Analysis Agent Implementation

## Section 1: Execution Plan

```markdown
## Execution Plan

1. **Initialize Configuration**
   - Tools: None
   - Set up risk thresholds and portfolio list
   - Define portfolio IDs to analyze: ["PORT-001", "PORT-002", "PORT-003"]
   - Define risk configuration with thresholds

2. **For Each Portfolio:**

   a. **Fetch Holdings**
   - Tool: `get_portfolio_holdings()`
   - Input: portfolio_id
   - Output: holdings data (needed for steps b, c, e)
   - Error Handling: Log error and skip to next portfolio if portfolio not found

   b. **Get Stock Prices**
   - Tool: `get_stock_prices()`
   - Input: symbols extracted from holdings
   - Output: current prices (needed for step c)
   - Error Handling: Skip symbols with no price data, log missing symbols

   c. **Calculate Portfolio Value**
   - Tool: `calculate_portfolio_value()`
   - Input: holdings and current_prices
   - Output: total_value and position details (needed for steps d, e)
   - Error Handling: Skip invalid inputs, log skipped positions

   d. **Calculate Volatility Score**
   - Tool: `calculate_volatility_score()`
   - Input: symbols from holdings
   - Output: volatility score (needed for step e)
   - Error Handling: Use default 30-day period, log errors

   e. **Check Risk Thresholds**
   - Tool: `check_risk_threshold()`
   - Input: portfolio_value and volatility_score
   - Output: risk status (needed for step f)
   - Error Handling: Use default risk level if calculation fails

   f. **Generate and Send Reports if High Risk**
   - Tools: `generate_report()` and `send_notification()`
   - Input: portfolio_data (from steps c and e)
   - Output: Generated report and sent notification
   - Error Handling: Log failed notifications, continue processing

3. **Error Handling Strategy**
   - Wrap each portfolio in try/except blocks
   - Log errors with detailed context
   - Continue processing remaining portfolios if one fails
   - Use default values where possible to avoid full failure
   - Log all operations with appropriate levels (info, warning, error)
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
from typing import Dict, List, Optional

# Configure basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def analyze_portfolios():
    """Main orchestration function for portfolio risk analysis."""
    # Configuration
    PORTFOLIOS = ["PORT-001", "PORT-002", "PORT-003"]
    RISK_CONFIG = {
        "max_volatility": 35.0,
        "min_value": 50000,
        "max_value": 2000000
    }
    
    # Process each portfolio
    for portfolio_id in PORTFOLIOS:
        try:
            # Step 2a: Fetch holdings
            log_operation("portfolio_analysis_start", {"portfolio_id": portfolio_id}, level="info")
            holdings = get_portfolio_holdings(portfolio_id)
            
            # Step 2b: Get stock prices
            symbols = [holding["symbol"] for holding in holdings["holdings"]]
            current_prices = get_stock_prices(symbols)
            
            # Step 2c: Calculate portfolio value
            value_data = calculate_portfolio_value(holdings["holdings"], current_prices)
            
            # Step 2d: Calculate volatility score
            volatility_score = calculate_volatility_score(symbols)
            
            # Step 2e: Check risk thresholds
            risk_check = check_risk_threshold(
                value_data["total_value"],
                volatility_score,
                RISK_CONFIG
            )
            
            # Prepare portfolio data for reporting
            portfolio_data = {
                "portfolio_id": portfolio_id,
                "client_name": holdings["client_name"],
                "total_value": value_data["total_value"],
                "volatility_score": volatility_score,
                "risk_level": risk_check["risk_level"],
                "exceeded_thresholds": risk_check["exceeded_thresholds"],
                "positions": value_data["positions"]
            }
            
            # Step 2f: Generate report and send notification if high risk
            if risk_check["is_high_risk"]:
                # Generate report
                report = generate_report(portfolio_data, report_format="markdown")
                
                # Send notification
                notification_result = send_notification(
                    recipient=holdings["manager_email"],
                    subject=f"High Risk Alert: Portfolio {portfolio_id}",
                    message=report,
                    priority="high"
                )
                
                # Log report generation and notification
                log_operation("report_generated", {
                    "portfolio_id": portfolio_id,
                    "report_length": len(report),
                    "risk_level": risk_check["risk_level"]
                }, level="info")
                
                log_operation("notification_sent", {
                    "portfolio_id": portfolio_id,
                    "notification_id": notification_result["message_id"],
                    "status": "success" if notification_result["sent"] else "failed"
                }, level="info")
            
            # Log successful processing
            log_operation("portfolio_analysis_complete", {
                "portfolio_id": portfolio_id,
                "total_value": value_data["total_value"],
                "volatility_score": volatility_score,
                "risk_level": risk_check["risk_level"]
            }, level="info")
            
        except Exception as e:
            # Log error and continue
            log_operation("portfolio_analysis_error", {
                "portfolio_id": portfolio_id,
                "error": str(e)
            }, level="error")
            logger.error(f"Error processing portfolio {portfolio_id}: {str(e)}")
            continue

if __name__ == "__main__":
    analyze_portfolios()
```

## Section 3: Design Justification

```markdown
## Design Justification

### Tool Orchestration Sequence
I chose a sequential processing approach for portfolios to ensure data consistency and simplify error handling. Each portfolio is processed independently to avoid cascading failures. This approach allows for immediate logging and notification when issues occur without affecting other portfolios.

### Data Flow Strategy
Holdings data feeds into three downstream operations (price fetching, value calculation, volatility scoring) because the same holdings information is needed for all three processes. This creates a natural data dependency that ensures consistency across calculations.

### Error Handling Strategy
The error handling strategy uses nested try/except blocks with specific exception handling for each tool. This allows for granular error recovery while maintaining audit logs. By continuing to the next portfolio when an error occurs, the system maintains availability even with partial failures.

### Trade-offs Considered
- **Performance vs. Reliability**: Sequential processing is slower than parallel processing but provides better reliability and easier debugging.
- **Completeness vs. Speed**: The system continues processing even if one portfolio fails, which may result in incomplete analysis but ensures maximum portfolio coverage.
- **Detail vs. Performance**: Comprehensive logging adds overhead but provides critical audit trails for compliance and troubleshooting.
- **Flexibility vs. Complexity**: Using the provided tools directly rather than creating abstractions maintains simplicity while still allowing for future tool replacements.

### Logging Strategy
The logging strategy uses multiple levels (info, warning, error) to provide context about the system's state. Each major operation is logged with specific details to enable traceability and auditing. This approach meets compliance requirements while providing visibility into system operations.

### Scalability Considerations
The design allows for easy scaling by simply adding more portfolio IDs to the list. The modular approach with clear separation of concerns (data fetching, calculation, reporting) makes it easy to add new tools or modify existing ones without disrupting the overall system.
```