## Section 1: Execution Plan (Markdown)

```markdown
## Execution Plan

1. **Initialize Configuration**
   - Tools: None
   - Set up risk thresholds and portfolio list.

2. **For Each Portfolio:**

   a. **Fetch Holdings**
      - Tool: `get_portfolio_holdings()`
      - Input: portfolio_id
      - Output: holdings data (needed for steps b, c, e)

   b. **Get Stock Prices**
      - Tool: `get_stock_prices()`
      - Input: symbols extracted from holdings
      - Output: current prices (needed for step c)

   c. **Calculate Portfolio Value and Positions**
      - Tool: `calculate_portfolio_value()`
      - Input: holdings, current_prices
      - Output: portfolio value and positions data (needed for step d)

   d. **Calculate Volatility Score**
      - Tool: `calculate_volatility_score()`
      - Input: symbols extracted from holdings, days=30
      - Output: volatility score (needed for step e)

   e. **Check Risk Thresholds**
      - Tool: `check_risk_threshold()`
      - Input: portfolio_value, volatility_score, risk_config
      - Output: risk check data (needed for steps f, g)

   f. **Generate Report**
      - Tool: `generate_report()`
      - Input: portfolio_data, report_format="markdown"
      - Output: markdown-formatted report

   g. **Send Notification**
      - Tool: `send_notification()`
      - Input: recipient (manager_email), subject, message=report_text, priority="high"
      - Output: notification result (none needed for further processing)

3. **Error Handling Strategy**
   - Wrap each portfolio processing in a try/except block.
   - Log errors and continue to the next portfolio.
   - If critical operations fail (e.g., fetching holdings), skip subsequent steps for that portfolio.

4. **Log Operations**
   - Use `log_operation()` at key points to record successful or failed operations.
```

## Section 2: Implementation (Python)

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
    """Main orchestration function."""
    
    # Step 1: Initialize Configuration
    risk_config = {
        "max_volatility": 35.0,
        "min_value": 50000,
        "max_value": 2000000
    }
    portfolios = ["PORT-001", "PORT-002", "PORT-003"]
    
    # Step 2: For Each Portfolio
    for portfolio_id in portfolios:
        try:
            log_operation("portfolio_analysis", {"portfolio_id": portfolio_id}, level="info")
            
            # a. Fetch Holdings
            holdings_data = get_portfolio_holdings(portfolio_id)
            if "holdings" not in holdings_data:
                raise ValueError("Invalid holdings data for portfolio.")
            
            # b. Get Stock Prices
            symbols = [holding["symbol"] for holding in holdings_data["holdings"]]
            prices = get_stock_prices(symbols)
            
            # c. Calculate Portfolio Value and Positions
            value_data = calculate_portfolio_value(holdings_data["holdings"], prices)
            
            # d. Calculate Volatility Score
            volatility_score = calculate_volatility_score(symbols, days=30)
            
            # e. Check Risk Thresholds
            risk_check_result = check_risk_threshold(
                value_data["total_value"],
                volatility_score,
                risk_config
            )
            
            if not risk_check_result["is_high_risk"]:
                continue
            
            # f. Generate Report
            portfolio_data = {
                "portfolio_id": holdings_data["portfolio_id"],
                "client_name": holdings_data["client_name"],
                "total_value": value_data["total_value"],
                "volatility_score": volatility_score,
                "risk_level": risk_check_result["risk_level"],
                "exceeded_thresholds": risk_check_result["exceeded_thresholds"],
                "positions": value_data["positions"]
            }
            
            report_text = generate_report(portfolio_data, report_format="markdown")
            
            # g. Send Notification
            notification_result = send_notification(
                holdings_data["manager_email"],
                f"High Risk Alert: Portfolio {portfolio_id}",
                report_text,
                priority="high"
            )
            
            log_operation("send_notification", {
                "portfolio_id": portfolio_id,
                "recipient": holdings_data["manager_email"],
                "notification_result": notification_result
            }, level="info")
        
        except ValueError as ve:
            log_operation("error", {"portfolio_id": portfolio_id, "error_message": str(ve)}, level="error")
            continue
        
        except Exception as e:
            log_operation("error", {"portfolio_id": portfolio_id, "error_message": str(e)}, level="critical")
            continue

if __name__ == "__main__":
    analyze_portfolios()
```

## Section 3: Design Justification (Markdown)

```markdown
## Design Justification

### Tool Orchestration Sequence
I chose to process portfolios sequentially rather than in parallel because each portfolio's analysis relies on the previous steps. This ensures that if any step fails, we can log the error and continue with the next portfolio without interrupting the entire process.

### Data Flow Strategy
Holdings data feeds into three downstream operations (price fetching, value calculation, volatility scoring) because:
- Stock prices are needed to calculate position values.
- Portfolio value is required for risk threshold checks.
- Symbols from holdings are used to calculate volatility scores.

### Error Handling Strategy Rationale
Error handling is crucial in an automated system where data might be unreliable or API calls might fail. By wrapping each portfolio's processing in a try/except block, we ensure that:
- Errors are logged with context (portfolio ID) for debugging.
- The system can continue processing other portfolios if one fails.
- Critical errors (e.g., invalid holdings data) are caught and skipped.

### Trade-offs Considered
- **Sequential Processing vs. Parallel**: Sequential ensures stability and easier error handling, but might be slower for a large number of portfolios. Parallel could improve performance but complicates error management.
- **Comprehensive Logging vs. Minimal Logs**: Comprehensive logging helps with debugging and auditing but increases log volume. A balanced approach is used here to capture key operations without cluttering the logs.
```

This plan, implementation, and justification should meet the requirements for a robust portfolio risk analysis system using the provided API tools.