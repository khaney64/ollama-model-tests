# Portfolio Risk Analysis Agent Implementation

## Section 1: Execution Plan

```markdown
## Execution Plan

1. **Initialize Configuration**
   - Tools: None
   - Define risk thresholds and portfolio list
   - Set up audit logging configuration

2. **For Each Portfolio:**

   a. **Fetch Holdings**
   - Tool: get_portfolio_holdings()
   - Input: portfolio_id
   - Output: Holdings data (needed for steps b, c, e)

   b. **Extract Symbols**
   - Tool: None
   - Input: Holdings data
   - Output: List of stock symbols (needed for step c)

   c. **Get Stock Prices**
   - Tool: get_stock_prices()
   - Input: Symbols list
   - Output: Current prices (needed for step d)

   d. **Calculate Portfolio Value**
   - Tool: calculate_portfolio_value()
   - Input: Holdings and prices
   - Output: Total value and position details (needed for step e)

   e. **Calculate Volatility Score**
   - Tool: calculate_volatility_score()
   - Input: Symbols list
   - Output: Volatility score (needed for step f)

   f. **Check Risk Thresholds**
   - Tool: check_risk_threshold()
   - Input: Portfolio value and volatility score
   - Output: Risk status (needed for step g)

   g. **Generate Report and Send Notification (if high risk)**
   - Tools: generate_report(), send_notification()
   - Input: Portfolio data and risk status
   - Output: Generated report and notification status

3. **Error Handling Strategy**
   - Wrap each portfolio in try/except blocks
   - Log errors with specific details
   - Continue processing remaining portfolios if one fails
   - Use specific exception handling for known errors
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

def analyze_portfolios():
    """Main orchestration function for portfolio risk analysis."""
    # Risk configuration
    risk_config = {
        "max_volatility": 35.0,
        "min_value": 50000,
        "max_value": 2000000
    }
    
    # List of portfolios to analyze
    portfolios = ["PORT-001", "PORT-002", "PORT-003"]
    
    for portfolio_id in portfolios:
        try:
            # Step 1: Log portfolio analysis start
            log_operation("portfolio_analysis_start", {"portfolio_id": portfolio_id}, "info")
            
            # Step 2: Fetch portfolio holdings
            holdings = get_portfolio_holdings(portfolio_id)
            log_operation("holdings_fetch", {"portfolio_id": portfolio_id, "success": True}, "info")
            
            # Step 3: Extract symbols for stock price lookup
            symbols = [holding["symbol"] for holding in holdings["holdings"]]
            
            # Step 4: Get current stock prices
            log_operation("stock_prices_fetch_start", {"portfolio_id": portfolio_id, "symbols": symbols}, "info")
            prices = get_stock_prices(symbols)
            log_operation("stock_prices_fetch_complete", {"portfolio_id": portfolio_id, "symbols": symbols, "prices": prices}, "info")
            
            # Step 5: Calculate portfolio value
            log_operation("portfolio_value_calc_start", {"portfolio_id": portfolio_id}, "info")
            value_data = calculate_portfolio_value(holdings["holdings"], prices)
            log_operation("portfolio_value_calc_complete", {"portfolio_id": portfolio_id, "total_value": value_data["total_value"]}, "info")
            
            # Step 6: Calculate volatility score
            log_operation("volatility_calc_start", {"portfolio_id": portfolio_id, "symbols": symbols}, "info")
            volatility_score = calculate_volatility_score(symbols, days=30)
            log_operation("volatility_calc_complete", {"portfolio_id": portfolio_id, "score": volatility_score}, "info")
            
            # Step 7: Check risk thresholds
            log_operation("risk_check_start", {"portfolio_id": portfolio_id}, "info")
            risk_check = check_risk_threshold(
                value_data["total_value"],
                volatility_score,
                risk_config
            )
            log_operation("risk_check_complete", {
                "portfolio_id": portfolio_id,
                "risk_level": risk_check["risk_level"],
                "exceeded_thresholds": risk_check["exceeded_thresholds"]
            }, "info")
            
            # Step 8: If high risk, generate report and send notification
            if risk_check["is_high_risk"]:
                # Prepare portfolio data for report
                portfolio_data = {
                    "portfolio_id": portfolio_id,
                    "client_name": holdings["client_name"],
                    "total_value": value_data["total_value"],
                    "volatility_score": volatility_score,
                    "risk_level": risk_check["risk_level"],
                    "exceeded_thresholds": risk_check["exceeded_thresholds"],
                    "positions": value_data["positions"]
                }
                
                # Generate report
                log_operation("report_generation_start", {"portfolio_id": portfolio_id}, "info")
                report = generate_report(portfolio_data, report_format="markdown")
                log_operation("report_generated", {"portfolio_id": portfolio_id, "report_length": len(report)}, "info")
                
                # Send notification
                log_operation("notification_send_start", {"portfolio_id": portfolio_id}, "info")
                send_result = send_notification(
                    recipient=holdings["manager_email"],
                    subject=f"High Risk Alert: Portfolio {portfolio_id}",
                    message=report,
                    priority="high"
                )
                log_operation("notification_sent", {
                    "portfolio_id": portfolio_id,
                    "recipient": holdings["manager_email"],
                    "success": send_result["sent"]
                }, "info" if send_result["sent"] else "error")
                
        except ValueError as ve:
            # Handle specific value errors
            log_operation("error_processing_portfolio", {
                "portfolio_id": portfolio_id,
                "error_type": "ValueError",
                "error_message": str(ve)
            }, "error")
            print(f"Error processing portfolio {portfolio_id}: {ve}")
        except Exception as e:
            # Handle other unexpected errors
            log_operation("error_processing_portfolio", {
                "portfolio_id": portfolio_id,
                "error_type": "UnexpectedError",
                "error_message": str(e)
            }, "error")
            print(f"Unexpected error processing portfolio {portfolio_id}: {e}")

if __name__ == "__main__":
    analyze_portfolios()
```

## Section 3: Design Justification

```markdown
## Design Justification

### Tool Orchestration Sequence
I chose to process portfolios sequentially rather than in parallel because:
- The operations are dependent (e.g., volatility calculation requires holdings data)
- The system needs to maintain a clear audit trail of operations
- Error handling is simpler with sequential processing
- Each portfolio is independent and can be processed in isolation

### Data Flow Strategy
Holdings data feeds into three downstream operations (price fetching, value calculation, volatility scoring) because:
- Holdings contain the symbols needed for stock price lookup
- Holdings and prices are required to calculate portfolio value
- Symbols from holdings are needed for volatility calculation
- Portfolio value and volatility score are required for risk threshold checking

### Error Handling Strategy
The error handling strategy is designed to:
- Isolate each portfolio's processing in its own try/except block
- Log all errors with detailed context (portfolio ID, error type, message)
- Continue processing remaining portfolios even if one fails
- Use specific exception handling for known errors (e.g., ValueErrors)
- Maintain audit logs with appropriate severity levels (info, warning, error)
- Handle skipped positions in calculate_portfolio_value gracefully

### Trade-offs Considered
- **Performance vs. Reliability**: Chose sequential processing for reliability over potential performance gains from parallel processing
- **Completeness vs. Efficiency**: Chose to handle all error cases explicitly even if it makes the code longer
- **Audit Trail vs. Performance**: Chose comprehensive logging over potential performance optimizations
- **Error Recovery vs. Complexity**: Implemented graceful error recovery with detailed logging rather than complex recovery mechanisms
```