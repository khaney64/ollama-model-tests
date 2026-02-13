# Section 1: Execution Plan

## Execution Plan

1. **Initialize Configuration**
   - Tools: None
   - Set up risk thresholds and portfolio list for processing

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
   - Input: total_value, volatility_score, and risk_config
   - Output: risk_check results (needed for step f)

   f. **Generate Report and Send Notification**
   - Tools: generate_report(), send_notification()
   - Input: portfolio_data and risk_check results
   - Output: formatted report and email notification

3. **Error Handling Strategy**
   - Wrap each portfolio in try/except
   - Log errors and continue to next portfolio
   - Gracefully handle missing stock prices and invalid portfolio IDs
   - Maintain audit logs for all operations

# Section 2: Implementation

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
    """Main orchestration function to analyze multiple portfolios."""
    # Define configuration parameters
    portfolio_ids = ["PORT-001", "PORT-002", "PORT-003"]
    risk_config = {
        "max_volatility": 35.0,
        "min_value": 50000,
        "max_value": 2000000
    }
    
    # Initialize audit log
    log_operation("portfolio_analysis_start", {"portfolio_ids": portfolio_ids}, level="info")
    
    for portfolio_id in portfolio_ids:
        try:
            # Step 1: Fetch portfolio holdings
            holdings = get_portfolio_holdings(portfolio_id)
            if not holdings:
                log_operation("portfolio_analysis", {"portfolio_id": portfolio_id, "status": "failed", "reason": "Invalid portfolio ID"}, level="error")
                continue
            
            # Step 2: Extract stock symbols from holdings
            symbols = [holding["symbol"] for holding in holdings["holdings"]]
            
            # Step 3: Get current stock prices
            current_prices = get_stock_prices(symbols)
            
            # Step 4: Calculate portfolio value and positions
            portfolio_value_data = calculate_portfolio_value(holdings["holdings"], current_prices)
            total_value = portfolio_value_data["total_value"]
            
            # Step 5: Calculate volatility score
            volatility_score = calculate_volatility_score(symbols)
            
            # Step 6: Check risk thresholds
            risk_check = check_risk_threshold(total_value, volatility_score, risk_config)
            
            # Step 7: Generate report and send notification if high-risk
            if risk_check["is_high_risk"]:
                # Prepare portfolio data for report
                portfolio_data = {
                    "portfolio_id": portfolio_id,
                    "client_name": holdings["client_name"],
                    "total_value": total_value,
                    "volatility_score": volatility_score,
                    "risk_level": risk_check["risk_level"],
                    "exceeded_thresholds": risk_check["exceeded_thresholds"],
                    "positions": portfolio_value_data["positions"]
                }
                
                # Generate markdown report
                report_text = generate_report(portfolio_data, report_format="markdown")
                
                # Send high-priority notification
                notification_result = send_notification(
                    recipient=holdings["manager_email"],
                    subject=f"High Risk Alert: Portfolio {portfolio_id}",
                    message=report_text,
                    priority="high"
                )
                
                # Log successful operations
                log_operation("report_generation", {"portfolio_id": portfolio_id, "status": "success"}, level="info")
                log_operation("notification_sent", {"portfolio_id": portfolio_id, "message_id": notification_result.get("message_id", "N/A")}, level="info")
            
            # Log successful risk check
            log_operation("risk_check", {"portfolio_id": portfolio_id, "risk_level": risk_check["risk_level"]}, level="info")
            
        except ValueError as ve:
            log_operation("portfolio_analysis", {"portfolio_id": portfolio_id, "error": str(ve)}, level="error")
        except Exception as e:
            log_operation("portfolio_analysis", {"portfolio_id": portfolio_id, "error": str(e)}, level="error")
    
    # Log completion of portfolio analysis
    log_operation("portfolio_analysis_end", {"status": "completed"}, level="info")

if __name__ == "__main__":
    analyze_portfolios()
```

# Section 3: Design Justification

## Design Justification

### Tool Orchestration Sequence
I chose to process portfolios sequentially rather than in parallel because:
- This approach simplifies error handling and ensures each portfolio is processed independently
- Sequential processing allows for better control over data flow between operations
- It maintains clarity in the execution plan for audit purposes

### Data Flow Strategy
Holdings data feeds into three downstream operations (price fetching, value calculation, volatility scoring) because:
- Holdings provide the list of stock symbols needed for price fetching
- Price data is required for both value calculation and volatility scoring
- Volatility score depends on the same symbols as the holdings

The risk check uses the portfolio value (from value calculation) and volatility score (from volatility scoring) to determine risk levels.

### Error Handling Strategy
I implemented comprehensive error handling by:
- Wrapping each portfolio in a try/except block
- Logging errors at the appropriate audit level
- Continuing to process remaining portfolios when one fails
- Handling specific ValueError cases for invalid inputs

This ensures the system remains robust and continues processing even when individual operations fail.

### Trade-offs Considered
- **Sequential vs Parallel Processing**: Chose sequential for simplicity and better error isolation
- **Data Handling**: Ensured all data transformations are explicit and documented
- **Error Handling**: Prioritized graceful degradation over stopping the entire process
- **Audit Logging**: Included detailed logging at every major operation to maintain an audit trail

This design balances simplicity, reliability, and maintainability while meeting all specified requirements.