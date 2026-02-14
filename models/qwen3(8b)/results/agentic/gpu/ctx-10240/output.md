## Execution Plan

## Execution Plan

1. **Initialize Configuration**
   - Tools: None
   - Set up risk thresholds and portfolio list

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
   - Output: total_value and positions (needed for report)

   d. **Calculate Volatility Score**
   - Tool: calculate_volatility_score()
   - Input: symbols and days=30
   - Output: volatility score (needed for risk check)

   e. **Check Risk Thresholds**
   - Tool: check_r't_risk_threshold()
   - Input: portfolio_value, volatility_score, risk_config
   - Output: risk check result (determines if report is needed)

   f. **Generate Report (if high-risk)**
   - Tool: generate_report()
   - Input: portfolio_data and report_format
   - Output: report string

   g. **Send Notification (if high-risk)**
   - Tool: send_notification()
   - Input: manager_email, subject, message, priority
   - Output: sent status

   h. **Log Operations**
   - Tool: log_operation()
   - Input: operation name, details, level

3. **Error Handling Strategy**
   - Wrap each portfolio in try/except
   - Log errors and continue to next portfolio
   - Handle invalid portfolio IDs, missing stock prices, failed notifications

---

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

def analyze_portfolios():
    """Main orchestration function to analyze portfolios and monitor risk."""
    # Configuration
    risk_config = {
        "max_volatility": 35.0,
        "min_value": 50000,
        "max_value": 2000000
    }
    portfolio_ids = ["PORT-001", "PORT-002", "PORT-003"]
    
    for portfolio_id in portfolio_ids:
        try:
            # Step 1: Fetch Holdings
            holdings = get_portfolio_holdings(portfolio_id)
            log_operation(
                "portfolio_analysis",
                {"portfolio_id": portfolio_id},
                level="info"
            )
        except ValueError as e:
            log_operation(
                "portfolio_analysis",
                {"portfolio_id": portfolio_id, "error": str(e)},
                level="error"
            )
            continue
        
        # Step 2: Get Stock Prices
        symbols = [position["symbol"] for position in holdings["holdings"]]
        try:
            prices = get_stock_prices(symbols)
            log_operation(
                "stock_prices",
                {"portfolio_id": portfolio_id, "symbols": symbols},
                level="info"
            )
        except ValueError as e:
            log_operation(
                "stock_prices",
                {"portfolio_id": portfolio_id, "error": str(e)},
                level="error"
            )
            continue
        
        # Step 3: Calculate Portfolio Value
        try:
            value_data = calculate_portfolio_value(holdings["holdings"], prices)
            log_operation(
                "portfolio_value",
                {"portfolio_id": portfolio_id},
                level="info"
            )
        except ValueError as e:
            log_operation(
                "portfolio_value",
                {"portfolio_id": portfolio_id, "error": str(e)},
                level="error"
            )
            continue
        
        # Step 4: Calculate Volatility Score
        try:
            volatility = calculate_volatility_score(symbols, days=30)
            log_operation(
                "volatility_score",
                {"portfolio_id": portfolio_id, "volatility": volatility},
                level="info"
            )
        except ValueError as e:
            log_operation(
                "volatility_score",
                {"portfolio_id": portfolio_id, "error": str(e)},
                level="error"
            )
            continue
        
        # Step 5: Check Risk Thresholds
        portfolio_value = value_data["total_value"]
        risk_check = check_risk_threshold(
            portfolio_value, volatility, risk_config
        )
        log_operation(
            "risk_check",
            {"portfolio_id": portfolio_id, "risk_check": risk_check},
            level="info"
        )
        
        # Step 6: Generate Report (if high-risk)
        if risk_check["is_high_risk"]:
            portfolio_data = {
                "portfolio_id": portfolio_id,
                "client_name": holdings["client_name"],
                "total_value": portfolio_value,
                "volatility_score": volatility,
                "risk_level": risk_check["risk_level"],
                "exceeded_thresholds": risk_check["exceeded_thresholds"],
                "positions": value_data["positions"]
            }
            
            try:
                report = generate_report(
                    portfolio_data, report_format="markdown"
                )
                log_operation(
                    "report_generation",
                    {"portfolio_id": portfolio_id},
                    level="info"
                )
            except ValueError as e:
                log_operation(
                    "report_generation",
                    {"portfolio_id": portfolio_id, "error": str(e)},
                    level="error"
                )
                continue
            
            # Step 7: Send Notification (if high-risk)
            try:
                result = send_notification(
                    recipient=holdings["manager_email"],
                    subject=f"High Risk Alert: Portfolio {portfolio_id}",
                    message=report,
                    priority="high"
                )
                log_operation(
                    "notification_sent",
                    {"portfolio_id": portfolio_id, "result": result},
                    level="info"
                )
            except ValueError as e:
                log_operation(
                    "notification_sent",
                    {"portfolio_id": portfolio_id, "error": str(e)},
                    level="error"
                )
                continue
            
            # Step 8: Log High-Risk Portfolio
            log_operation(
                "high_risk_portfolio",
                {"portfolio_id": portfolio_id, "risk_level": risk_check["risk_level"]},
                level="warning"
            )

if __name__ == "__main__":
    analyze_portfolios()
```

---

## Design Justification

### Tool Orchestration Sequence
I chose to process portfolios sequentially rather than in parallel because:
1. Each portfolio requires unique data that's not shared between them (e.g., different client names and managers)
2. Sequential processing ensures we can handle errors for one portfolio without affecting others
3. This approach simplifies data flow management and error isolation

### Data Flow Strategy
Holdings data feeds into three downstream operations (price fetching, value calculation, volatility scoring) because:
1. Holdings contain the list of symbols needed for stock price lookup
2. Portfolio value calculation requires both holdings and current prices
3. Volatility score calculation needs the same symbols used in holdings

The calculated portfolio value and volatility score are then used in the risk threshold check, which determines whether a report and notification are needed.

### Error Handling Strategy
I implemented comprehensive error handling by:
1. Wrapping each portfolio processing in try/except blocks
2. Logging errors with appropriate levels (error/warning/info)
3. Continuing processing for other portfolios when one fails
4. Handling specific error cases for each tool as specified in their documentation

### Trade-offs Considered
1. **Performance vs. Reliability**: Chose sequential processing over parallel to ensure reliability and easier error handling
2. **Data Completeness**: Ensured all required data is collected before making decisions about risk levels
3. **Error Resilience**: Designed the system to handle missing data gracefully without crashing
4. **Audit Trail**: Implemented logging at every major operation to maintain a complete record of all actions

This approach balances thoroughness with efficiency, ensuring that the system can handle real-world data inconsistencies while maintaining accurate risk analysis and reporting.