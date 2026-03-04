## Execution Plan

### Step-by-Step Execution Plan

1. **Initialize Configuration**
   - Tools: None
   - Set up risk thresholds and portfolio list.

2. **For Each Portfolio:**

   a. **Fetch Holdings**
      - Tool: `get_portfolio_holdings()`
      - Input: `portfolio_id`
      - Output: holdings data (needed for steps b, c, e)

   b. **Get Stock Prices**
      - Tool: `get_stock_prices()`
      - Input: symbols extracted from holdings
      - Output: current prices (needed for step c)

   c. **Calculate Portfolio Value and Position Details**
      - Tool: `calculate_portfolio_value()`
      - Inputs: holdings data, current prices

   d. **Calculate Volatility Score**
      - Tool: `calculate_volatility_score()`
      - Input: portfolio symbols from holdings
      - Output: volatility score (needed for step e)

   e. **Check Risk Thresholds and Generate Reports**
      - Tool: `check_risk_threshold()`
      - Inputs: total value, volatility score, risk configuration
      - Output: high-risk status

   f. **Generate Report and Send Notification**
      - Tools: `generate_report()`, `send_notification()`
      - Input: portfolio data from steps c and d
      - Outputs: formatted report string and email notification details (needed for step g)

3. **Error Handling Strategy**
   - Wrap each portfolio in a try/except block to handle exceptions such as invalid portfolio IDs, missing stock price data, or failed notifications.
   - Log errors and continue processing the next portfolio.

4. **Maintain Audit Trail**
   - Tools: `log_operation()`
   - Log major operations including portfolio analysis start/completion, risk threshold checks, report generation, and notification sending.

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
    """Main orchestration function."""
    risk_config = {
        "max_volatility": 35.0,
        "min_value": 50000,
        "max_value": 2000000
    }
    
    portfolios_to_analyze = ["PORT-001", "PORT-002", "PORT-003"]

    for portfolio_id in portfolios_to_analyze:
        try:
            log_operation("portfolio_analysis_start", {"portfolio_id": portfolio_id})

            # Step 2a: Fetch Holdings
            holdings_data = get_portfolio_holdings(portfolio_id)
            
            if not holdings_data:
                log_operation("error", {"message": f"No holdings data found for {portfolio_id}"})
                continue

            symbols = [holding["symbol"] for holding in holdings_data["holdings"]]
            log_operation("holdings_fetched", {"portfolio_id": portfolio_id, "symbols": symbols})

            # Step 2b: Get Stock Prices
            prices = get_stock_prices(symbols)
            if not all(prices.values()):
                log_operation("error", {"message": f"Missing stock price data for some symbols in {portfolio_id}"})
                continue

            log_operation("prices_fetched", {"portfolio_id": portfolio_id, "symbols_with_prices": list(prices.items())})

            # Step 2c: Calculate Portfolio Value and Position Details
            value_data = calculate_portfolio_value(holdings_data["holdings"], prices)
            if not value_data:
                log_operation("error", {"message": f"No value data calculated for {portfolio_id}"})
                continue

            total_value, positions = value_data["total_value"], [pos["symbol"] for pos in value_data["positions"]]
            log_operation("value_calculated", {"portfolio_id": portfolio_id, "total_value": total_value})

            # Step 2d: Calculate Volatility Score
            volatility_score = calculate_volatility_score(symbols)
            if volatility_score is None:
                log_operation("error", {"message": f"Failed to calculate volatility score for {portfolio_id}"})
                continue

            log_operation("volatility_calculated", {"portfolio_id": portfolio_id, "volatility_score": volatility_score})

            # Step 2e: Check Risk Thresholds
            risk_check = check_risk_threshold(total_value, volatility_score, risk_config)
            if not risk_check:
                log_operation("error", {"message": f"Failed to check risk thresholds for {portfolio_id}"})
                continue

            is_high_risk, exceeded_thresholds, _ = risk_check["is_high_risk"], risk_check["exceeded_thresholds"]
            
            # Step 2f: Generate Report and Send Notification
            if is_high_risk:
                portfolio_data = {
                    "portfolio_id": portfolio_id,
                    "client_name": holdings_data["client_name"],
                    "total_value": total_value,
                    "volatility_score": volatility_score,
                    "risk_level": risk_check["risk_level"],
                    "exceeded_thresholds": exceeded_thresholds,
                    "positions": positions
                }
                report = generate_report(portfolio_data, report_format="markdown")
                
                log_operation("report_generated", {"portfolio_id": portfolio_id})
                
                notification_result = send_notification(
                    holdings_data["manager_email"],
                    f"High Risk Alert: Portfolio {portfolio_id}",
                    report,
                    priority="high"
                )
                
                if not notification_result:
                    log_operation("error", {"message": f"Failed to send notification for {portfolio_id}"})
                    continue

                log_operation("notification_sent", {"portfolio_id": portfolio_id, "status": "success"})

            # Log completion
            log_operation("portfolio_analysis_complete", {"portfolio_id": portfolio_id})
        except Exception as e:
            log_operation("error", {"message": f"An error occurred while analyzing {portfolio_id}: {str(e)}"})
            continue

if __name__ == "__main__":
    analyze_portfolios()
```

## Design Justification

### Tool Orchestration Sequence
I chose to process portfolios sequentially rather than in parallel because:
- Sequential processing ensures that each portfolio is fully analyzed before moving on to the next one, which helps in maintaining a clear audit trail and error handling strategy.

### Data Flow Strategy
Holdings data feeds into three downstream operations (price fetching, value calculation, volatility scoring) because:
- It provides necessary context for calculating the total value of the portfolio.
- It ensures that all relevant details are collected before applying risk thresholds.

### Error Handling Strategy Rationale
Handling errors by wrapping each portfolio in a try/except block is effective because:
- It allows us to catch and log any unexpected issues, providing transparency into what went wrong.
- We can continue processing other portfolios even if one fails, ensuring that no single error stops the entire process.

### Trade-offs Considered
- **Parallel vs. Sequential Processing**: While parallel processing could reduce overall execution time, it would complicate error handling and logging. Sequential processing is simpler to manage and aligns well with our requirement for maintaining a clear audit trail.
- **Data Integrity Checks**: By validating data at each step (e.g., ensuring holdings are not empty), we ensure that the analysis is based on accurate information.

By following this structured approach, we can effectively monitor multiple portfolios, identify high-risk ones, and notify relevant parties while maintaining thorough documentation of our actions.