## Execution Plan

### Step-by-Step Execution Plan

1. **Initialize Configuration**
   - Tools: None
   - Set up risk thresholds and portfolio list

2. **For Each Portfolio:**

   a. **Fetch Holdings**
   - Tool: `get_portfolio_holdings()`
   - Input: portfolio_id
   - Output: holdings data (needed for steps b, c, e)

   b. **Get Stock Prices**
   - Tool: `get_stock_prices()`
   - Input: symbols extracted from holdings
   - Output: current prices (needed for step c)

   c. **Calculate Portfolio Value**
   - Tool: `calculate_portfolio_value()`
   - Input: holdings and current_prices
   - Output: total_value and position details (needed for steps d, f)

   d. **Calculate Volatility Score**
   - Tool: `calculate_volatility_score()`
   - Input: symbols from holdings
   - Output: volatility score (needed for step f)

   e. **Check Risk Thresholds**
   - Tool: `check_risk_threshold()`
   - Input: portfolio_value, volatility_score, risk_config
   - Output: risk assessment (needed for step g)

   f. **Generate Report (if high-risk)**
   - Tool: `generate_report()`
   - Input: portfolio_data and report_format
   - Output: formatted report (needed for step g)

   g. **Send Notification (if high-risk)**
   - Tool: `send_notification()`
   - Input: recipient, subject, message, priority
   - Output: notification status

3. **Error Handling Strategy**
   - Wrap each portfolio in try/except
   - Log errors and continue to next portfolio
   - Use `log_operation()` for all major operations
   - Ensure data flow between steps is preserved
   - Handle missing data gracefully

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

# Risk configuration as per the problem statement
RISK_CONFIG = {
    "max_volatility": 35.0,
    "min_value": 50000,
    "max_value": 2000000
}

# List of portfolios to analyze
PORTFOLIOS = ["PORT-001", "PORT-002", "PORT-003"]

def analyze_portfolios():
    """Main orchestration function to analyze portfolios and manage risk."""
    for portfolio_id in PORTFOLIOS:
        try:
            # Log portfolio analysis start
            log_operation("portfolio_analysis_start", {"portfolio_id": portfolio_id}, "info")
            
            # Step 1: Fetch portfolio holdings
            holdings = get_portfolio_holdings(portfolio_id)
            if not holdings:
                raise ValueError(f"Portfolio {portfolio_id} not found")
            
            # Step 2: Get current stock prices for all holdings
            symbols = [h["symbol"] for h in holdings["holdings"]]
            prices = get_stock_prices(symbols)
            
            # Step 3: Calculate portfolio value and position details
            value_data = calculate_portfolio_value(holdings["holdings"], prices)
            if not value_data or "total_value" not in value_data:
                raise ValueError(f"Failed to calculate portfolio value for {portfolio_id}")
            
            # Step 4: Calculate volatility score
            volatility = calculate_volatility_score(symbols)
            if volatility is None:
                raise ValueError(f"Failed to calculate volatility for {portfolio_id}")
            
            # Step 5: Check risk thresholds
            risk_check = check_risk_threshold(
                value_data["total_value"],
                volatility,
                RISK_CONFIG
            )
            
            # Step 6: Prepare portfolio data for report
            portfolio_data = {
                "portfolio_id": portfolio_id,
                "client_name": holdings["client_name"],
                "total_value": value_data["total_value"],
                "volatility_score": volatility,
                "risk_level": risk_check["risk_level"],
                "exceeded_thresholds": risk_check["exceeded_thresholds"],
                "positions": value_data["positions"]
            }
            
            # Log risk check result
            log_operation(
                "risk_check",
                {
                    "portfolio_id": portfolio_id,
                    "risk_level": risk_check["risk_level"],
                    "exceeded_thresholds": risk_check["exceeded_thresholds"]
                },
                "warning" if risk_check["is_high_risk"] else "info"
            )
            
            # Step 7: Generate report and send notification if high-risk
            if risk_check["is_high_risk"]:
                # Generate markdown report
                report = generate_report(portfolio_data, "markdown")
                
                # Send high-priority notification
                notification_result = send_notification(
                    recipient=holdings["manager_email"],
                    subject=f"High Risk Alert: Portfolio {portfolio_id}",
                    message=report,
                    priority="high"
                )
                
                # Log notification result
                log_operation(
                    "notification_sent",
                    {
                        "portfolio_id": portfolio_id,
                        "message_id": notification_result.get("message_id", "N/A"),
                        "sent": notification_result.get("sent", False)
                    },
                    "info"
                )
            
            # Log portfolio analysis completion
            log_operation("portfolio_analysis_complete", {"portfolio_id": portfolio_id}, "info")
            
        except Exception as e:
            # Log error and continue processing other portfolios
            log_operation(
                "portfolio_analysis_error",
                {
                    "portfolio_id": portfolio_id,
                    "error": str(e)
                },
                "error"
            )
            continue

if __name__ == "__main__":
    analyze_portfolios()
```

## Design Justification

### Tool Orchestration Sequence
I chose to process portfolios sequentially rather than in parallel because:
- Sequential processing simplifies error handling and audit logging
- Each portfolio has unique holdings and manager information
- The risk assessment requires complete data from all previous steps

### Data Flow Strategy
Holdings data feeds into three downstream operations (price fetching, value calculation, volatility scoring) because:
- Holdings contain the list of symbols needed for price data
- Price data is required for value calculation
- Symbols from holdings are needed for volatility scoring
- Portfolio value and volatility score are required for risk assessment

The calculated metrics are then used to generate reports and notifications, ensuring data flows logically through the system.

### Error Handling Strategy
I implemented comprehensive error handling by:
- Wrapping each portfolio in a try/except block
- Logging all errors with detailed context
- Continuing processing for other portfolios when one fails
- Using the `log_operation()` function for all major operations

This approach ensures the system remains robust while maintaining audit trail requirements.

### Trade-offs Considered
- Chose sequential processing over parallel to simplify dependency management
- Used the most granular data from each step to ensure accurate risk assessment
- Prioritized error logging over performance optimization for audit requirements
- Implemented graceful degradation by continuing processing when individual steps fail