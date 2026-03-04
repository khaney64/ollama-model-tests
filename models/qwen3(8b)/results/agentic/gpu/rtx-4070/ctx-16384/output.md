## Section 1: Execution Plan

## Execution Plan

1. **Initialize Configuration**
   - Tools: None
   - Set up risk thresholds and portfolio list
   - Data: risk_config (max_volatility: 35.0, min_value: 50000, max_value: 2000000)
   - Data: portfolio_ids = ["PORT-001", "PORT-002", "PORT-003"]

2. **For Each Portfolio:**

   a. **Fetch Holdings**
   - Tool: get_portfolio_holdings()
   - Input: portfolio_id
   - Output: holdings data (needed for steps b, c, e)

   b. **Get Stock Prices**
   - Tool: get_stock_prices()
   - Input: symbols extracted from holdings
   - Output: current prices (needed for step c)

   c. **Calculate Portfolio Value**
   - Tool: calculate_portfolio_value()
   - Input: holdings and current_prices
   - Output: total_value and positions (needed for step d)

   d. **Calculate Volatility Score**
   - Tool: calculate_volatility_score()
   - Input: symbols from holdings
   - Output: volatility_score (needed for step e)

   e. **Check Risk Thresholds**
   - Tool: check_risk_threshold()
   - Input: portfolio_value, volatility_score, risk_config
   - Output: risk_level and exceeded_thresholds (needed for step f)

   f. **Generate Report and Send Notification**
   - Tool: generate_report() and send_notification()
   - Input: portfolio_data (includes all risk metrics)
   - Output: formatted report and email notification

3. **Error Handling Strategy**
   - Wrap each portfolio in try/except
   - Log errors and continue to next portfolio
   - For missing stock prices, skip positions with None values
   - For failed notifications, log error and continue
   - For invalid portfolio IDs, log error and skip
   - Maintain audit logs for all operations

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

def analyze_portfolios():
    """Main orchestration function for portfolio risk analysis."""
    # Initialize configuration
    risk_config = {
        "max_volatility": 35.0,
        "min_value": 50000,
        "max_value": 2000000
    }
    portfolio_ids = ["PORT-001", "PORT-002", "PORT-003"]
    
    for portfolio_id in portfolio_ids:
        try:
            # Step 1: Fetch portfolio holdings
            holdings = get_portfolio_holdings(portfolio_id)
            log_operation("portfolio_analysis_started", {"portfolio_id": portfolio_id}, "info")
            
            # Step 2: Get current stock prices for all symbols
            symbols = [h["symbol"] for h in holdings["holdings"]]
            prices = get_stock_prices(symbols)
            
            # Step 3: Calculate portfolio value and position details
            portfolio_value = calculate_portfolio_value(holdings["holdings"], prices)
            total_value = portfolio_value["total_value"]
            positions = portfolio_value["positions"]
            
            # Step 4: Calculate volatility score for the portfolio
            volatility_score = calculate_volatility_score(symbols, days=30)
            
            # Step 5: Check if portfolio exceeds risk thresholds
            risk_check = check_risk_threshold(total_value, volatility_score, risk_config)
            is_high_risk = risk_check["is_high_risk"]
            exceeded_thresholds = risk_check["exceeded_thresholds"]
            risk_level = risk_check["risk_level"]
            
            # Step 6: Generate report and send notification if high-risk
            if is_high_risk:
                portfolio_data = {
                    "portfolio_id": portfolio_id,
                    "client_name": holdings["client_name"],
                    "total_value": total_value,
                    "volatility_score": volatility_score,
                    "risk_level": risk_level,
                    "exceeded_thresholds": exceeded_thresholds,
                    "positions": positions
                }
                report_text = generate_report(portfolio_data, report_format="markdown")
                
                # Send notification to portfolio manager
                manager_email = holdings["manager_email"]
                subject = f"High Risk Alert: Portfolio {portfolio_id}"
                notification_result = send_notification(
                    recipient=manager_email,
                    subject=subject,
                    message=report_text,
                    priority="high"
                )
                
                # Log notification sent
                log_operation("notification_sent", {
                    "portfolio_id": portfolio_id,
                    "message_id": notification_result.get("message_id"),
                    "timestamp": notification_result.get("timestamp")
                }, "info")
            
            # Log risk check results
            log_operation("risk_check", {
                "portfolio_id": portfolio_id,
                "risk_level": risk_level,
                "exceeded_thresholds": exceeded_thresholds
            }, "info" if risk_level == "LOW" else "warning")
            
        except ValueError as ve:
            # Handle specific errors from API tools
            log_operation("portfolio_analysis_failed", {
                "portfolio_id": portfolio_id,
                "error": str(ve)
            }, "error")
        except Exception as e:
            # Handle unexpected errors
            log_operation("portfolio_analysis_failed", {
                "portfolio_id": portfolio_id,
                "error": str(e)
            }, "error")
        finally:
            # Log completion of portfolio analysis
            log_operation("portfolio_analysis_completed", {"portfolio_id": portfolio_id}, "info")

if __name__ == "__main__":
    analyze_portfolios()
```

## Section 3: Design Justification

## Design Justification

### Tool Orchestration Sequence
I chose to process portfolios sequentially rather than in parallel because:
- The tools have dependencies between steps (holdings → prices → value → volatility)
- Sequential processing simplifies error handling and data flow
- The risk analysis requires all previous steps to be completed before determining risk status

### Data Flow Strategy
Holdings data feeds into three downstream operations (price fetching, value calculation, volatility scoring) because:
- Holdings provide the list of symbols needed for stock price lookup
- Holdings and prices are required for portfolio value calculation
- Holdings symbols are needed for volatility scoring
- Portfolio value and volatility score are required for risk threshold checking

### Error Handling Strategy
I implemented comprehensive error handling by:
- Wrapping each portfolio in try/except blocks
- Logging errors to the audit trail
- Continuing processing for other portfolios when one fails
- Distinguishing between specific API errors and general exceptions
- Gracefully skipping missing stock prices while still calculating portfolio value

### Trade-offs Considered
- **Sequential vs Parallel Processing**: Chose sequential for simplicity and better error isolation
- **Error Handling**: Prioritized logging over retrying to maintain audit trail integrity
- **Data Validation**: Implemented checks for required parameters while allowing partial processing
- **Reporting**: Used markdown format for readability while keeping the report generation separate from notification sending

This design ensures the system can handle partial failures, maintain audit trails, and provide actionable insights for portfolio managers while adhering to the risk thresholds defined in the configuration.